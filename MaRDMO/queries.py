'''Function that query Data'''
import logging
from multiprocessing.pool import ThreadPool
from django.core.cache import cache

import requests

from .getters import get_url, get_user_entries
from .helpers import extract_parts, rank_by_search_term

logger = logging.getLogger(__name__)

def query_item(label, description, api = get_url('mardi', 'api')):
    '''API request returning an Item whose label or alias matches,
       and with matching description.'''
    # Only check Items with description
    if not description or description == 'No Description Provided!':
        return None

    # Get data from API
    data = query_api(api, label)

    # Normalize input label for comparison (case insensitive)
    norm_label = label.strip().lower()

    matched_items = []
    for item in data:
        item_label = item.get('label', '').strip().lower()
        item_description = item.get('description', '').strip()
        item_aliases = [alias.strip().lower() for alias in item.get('aliases', [])]

        # Check label or alias match AND description match
        if (
            (item_label == norm_label or norm_label in item_aliases)
            and item_description == description
        ):
            matched_items.append(item)

    if matched_items:
        return matched_items[0]['id']

    return None

def query_api(api_url, search_term, timeout=5):
    """API requests returning all Items with matching label."""
    try:
        response = requests.get(
            api_url,
            params={
                'action': 'wbsearchentities',
                'format': 'json',
                'language': 'en',
                'type': 'item',
                'limit': 10,
                'search': search_term
            },
            headers={'User-Agent': 'MaRDMO (https://zib.de; reidelbach@zib.de)'},
            timeout=timeout
        )
        response.raise_for_status()  # Raise an error on bad HTTP status codes
        try:
            return response.json().get('search', [])
        except ValueError:
            # Malformed JSON
            logger.error("Failed to parse JSON.")
    except requests.exceptions.RequestException as e:
        logger.error("Request failed due to %s", e)

    return []

def query_sparql(query, sparql_endpoint):
    '''SPARQL request returning all Items with matching properties.'''
    if not sparql_endpoint:
        logger.warning("SPARQL query attempted without a valid endpoint.")
        return []

    try:
        response = requests.post(
            sparql_endpoint,
            data=query.encode("utf-8"),
            headers={
                "User-Agent": "MaRDMO (https://zib.de; reidelbach@zib.de)",
                "Content-Type": "application/sparql-query; charset=UTF-8",
                "Accept": "application/sparql-results+json"
            },
            timeout = 60
        )
        # Check if request was successful
        if response.status_code == 200:
            return response.json().get('results', {}).get('bindings', [])

        logger.error(
            "SPARQL request to %s failed with status %s: %s",
            sparql_endpoint,
            response.status_code,
            response.text,
        )

        return []

    except requests.exceptions.ConnectionError:
        logger.error(
            "SPARQL query failed: Unable to connect to the %s.",
            sparql_endpoint
        )

    except requests.exceptions.RequestException as e:
        logger.exception("SPARQL request failed: %s", e)

    return []

def query_sparql_pool(query_input):
    '''Pooled SPARQL request returning all items with matching properties 
       from different endpoints'''
    pool = ThreadPool(processes = len(query_input))
    # Map each endpoint's query and store results in a dictionary
    results = pool.map(lambda args: query_sparql(*args), query_input.values())
    data = dict(zip(query_input.keys(), results))
    return data

def query_sources(search, item_class=None, sources=None, not_found=True):
    '''Query specified sources for items and return sorted results.

    item_class – QID string or list of QID strings used for class-filtered
                 search on MaRDI, e.g. 'Q42' or ['Q42', 'Q43'].
                 Wikidata is always queried by label/description only
                 (class classification on Wikidata is too inconsistent).
    sources    – list of sources to query; defaults to ['mardi', 'wikidata'].
    '''
    if sources is None:
        sources = ['mardi', 'wikidata']

    source_functions = {}
    if 'mardi' in sources:
        source_functions['mardi'] = lambda s: query_api_per_class(s, item_class)
    if 'wikidata' in sources:
        source_functions['wikidata'] = lambda s: query_api(get_url('wikidata', 'api'), s)

    pool = ThreadPool(processes=len(source_functions))
    results = pool.map(lambda func: func(search), source_functions.values())
    results_dict = dict(zip(source_functions.keys(), results))

    options = []
    for source in sources:
        if source not in results_dict:
            continue
        raw = results_dict[source][:25]
        if source == 'wikidata':
            # query_api returns raw Wikibase search dicts; format them here
            display_key = 'display'
            raw = [
                {
                    'id':   f"wikidata:{r['id']}",
                    'text': (f"{r[display_key].get('label', {}).get('value', 'No Label Provided!')}"
                             f" ({r[display_key].get('description', {}).get('value', 'No Description Provided!')})"
                             f" [wikidata]"),
                }
                for r in raw
                if display_key in r
            ]
        options += raw

    options.sort(key=lambda opt: rank_by_search_term(opt, search))

    if not_found:
        options = [{'id': 'not found', 'text': 'not found'}] + options

    return options

def query_sources_with_user_additions(search, project, setup):
    '''Fetch options from KG, user-defined fields, and allow creation.'''
    if setup['sources'] is None:
        setup['sources'] = ['mardi', 'wikidata']

    # Query external sources
    try:
        options = query_sources(
            search=search,
            item_class=setup['item_class'],
            sources=setup['sources'],
            not_found=False,
        )
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.error("Query sources failed: %s", e)
        options = []

    # Get or build user entries dictionary
    cache_key = f"user_entries_{project.id}_{','.join(setup['query_attributes'])}"
    dic = cache.get(cache_key)

    if dic is None:
        logger.debug("Cache miss for %s, querying database", cache_key)
        dic = query_user_entries(project, setup)
        cache.set(cache_key, dic, timeout=180)
        logger.debug("Cached user entries for %s", cache_key)
    else:
        logger.debug("Cache hit for %s", cache_key)

    # Filter and merge options
    options_user = [
        {'id': value['id'], 'text': key}
        for key, value in dic.items()
        if search.lower() in key.lower()
    ]
    options = options_user + options

    # Add creation option if needed
    if setup['creation']:
        creation_option = {'id': 'not found', 'text': search}
        if creation_option not in options:
            options.insert(0, creation_option)

    return options

def query_user_entries(project, setup):
    '''Collect user entries from database and build options dictionary.'''
    dic = {}

    for query_attribute in setup['query_attributes']:
        # Get entries from database
        values = get_user_entries(
            project=project,
            query_attribute=query_attribute,
            values={}
        )

        # Align id/name/description by numeric index
        entries_by_idx = {}
        for value_id in values['id']:
            idx = value_id.set_index
            entries_by_idx.setdefault(idx, {})['id'] = value_id

        for value_name in values['name']:
            idx = int(value_name.set_prefix)
            entries_by_idx.setdefault(idx, {})['name'] = value_name

        for value_desc in values['description']:
            idx = int(value_desc.set_prefix)
            entries_by_idx.setdefault(idx, {})['description'] = value_desc

        # Process aligned entries
        for idx in sorted(entries_by_idx.keys()):
            entry = entries_by_idx[idx]

            if not entry['id'].text:
                continue

            # Build item
            if entry['id'].text == 'not found':
                # User-defined item
                label = entry['name'].text or "No Label Provided!"
                description = entry['description'].text or "No Description Provided!"
                item_id = 'not found'
                source = 'user'
            else:
                # External ID item
                label, description, source = extract_parts(entry['id'].text)
                _, item_id = entry['id'].external_id.split(':')
                item_id = f"{source}:{item_id}"

            # Add to dictionary if not from primary sources
            if source not in setup['sources']:
                if source == 'user':
                    dic[f"{label} ({description})"] = {'id': item_id}
                else:
                    dic[f"{label} ({description}) [{source}]"] = {'id': item_id}

    return dic

def query_api_per_class(search_term: str, item_class) -> list[dict]:
    '''Search the MaRDI portal for items belonging to one or more classes.

    item_class – a single QID string or a list of QID strings.  Multiple
                 classes are combined with OR: haswbstatement:P31=Q1|P31=Q2.
    Returns list of dicts with id and text matching the format used by query_sources.
    '''
    if isinstance(item_class, str):
        item_class = [item_class]

    class_filter = '|'.join(f'P31={qid}' for qid in item_class)
    api_url      = get_url('mardi', 'api')

    try:
        search_resp = requests.get(
            api_url,
            params={
                'action':      'query',
                'list':        'search',
                'srsearch':    f'{search_term}* haswbstatement:{class_filter}',
                'srnamespace': 120,
                'srlimit':     50,
                'srprop':      'snippet',
                'format':      'json',
            },
            headers={'User-Agent': 'MaRDMO (https://zib.de; reidelbach@zib.de)'},
            timeout=5,
        )
        search_resp.raise_for_status()
        hits = search_resp.json().get('query', {}).get('search', [])
    except requests.exceptions.RequestException as e:
        logger.error("Class-based MaRDI search failed: %s", e)
        return []

    if not hits:
        return []

    qids = [hit['title'].removeprefix('Item:') for hit in hits]

    try:
        entity_resp = requests.get(
            api_url,
            params={
                'action':    'wbgetentities',
                'ids':       '|'.join(qids),
                'props':     'labels|descriptions',
                'languages': 'en',
                'format':    'json',
            },
            headers={'User-Agent': 'MaRDMO (https://zib.de; reidelbach@zib.de)'},
            timeout=5,
        )
        entity_resp.raise_for_status()
        entities = entity_resp.json().get('entities', {})
    except requests.exceptions.RequestException as e:
        logger.error("MaRDI entity fetch failed: %s", e)
        return []

    results = []
    for qid in qids:
        entity      = entities.get(qid, {})
        label       = entity.get('labels',       {}).get('en', {}).get('value', qid)
        description = entity.get('descriptions', {}).get('en', {}).get('value',
                                                                        'No Description Provided!')
        results.append({
            'id':   f'mardi:{qid}',
            'text': f'{label} ({description}) [mardi]',
        })

    return results
