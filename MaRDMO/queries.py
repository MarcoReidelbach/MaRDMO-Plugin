'''Function that query Data'''

import logging
from multiprocessing.pool import ThreadPool

import requests
from rdmo.domain.models import Attribute

from .algorithm.sparql import queryProviderAL
from .config import BASE_URI, endpoint
from .helpers import extract_parts

logger = logging.getLogger(__name__)

def query_item(label, description, api=endpoint['mardi']['api']):
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
            data=query,
            headers={
                "User-Agent": "MaRDMO (https://zib.de; reidelbach@zib.de)",
                "Content-Type": "application/sparql-query",
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

def query_sources(search, query_id = '', sources = None, not_found = True):
    '''Helper function to query specified sources and process results.'''

    if sources is None:
        # Set default Sources
        sources = ['mardi', 'wikidata']

    def process_result(result, source):
        '''Function to process the result and return a dictionary with id and text'''
        display = result['display']
        label = display.get('label', {}).get('value', 'No Label Provided!')
        description = display.get('description', {}).get('value', 'No Description Provided!')
        return {
            'id': f"{source}:{result['id']}",
            'text': f"{label} ({description}) [{source}]"        
        }

    source_functions = {
        'wikidata': lambda s: query_api(endpoint['wikidata']['api'], s),
        'mardi': lambda s: query_api(endpoint['mardi']['api'], s),
        'mathalgodb': lambda s: query_provider(s, queryProviderAL[query_id], 'mathalgodb')
    }

    # Filter only specified sources
    queries = [source_functions[source] for source in sources if source in source_functions]

    # Use ThreadPool to make concurrent API requests
    pool = ThreadPool(processes=len(queries))
    results = pool.map(lambda func: func(search), queries)

    # Unpack results based on available sources
    results_dict = dict(zip(sources, results))

    # Process results to fit RDMO Provider Output Requirements
    options = []

    if 'mathalgodb' in results_dict:
        options += results_dict['mathalgodb'][:15]

    if 'mardi' in results_dict:
        options += [process_result(result, 'mardi') for result in results_dict['mardi'][:15]]

    if 'wikidata' in results_dict:
        options += [process_result(result, 'wikidata') for result in results_dict['wikidata'][:15]]

    if not_found:
        options = [{'id': 'not found', 'text': 'not found'}] + options

    return options

def query_provider(search, query, source):
    """
    Dynamic query of MathModDB and MathAlgoDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathAlgoDB knowledge graph
    results = query_sparql(
        query = query,
        sparql_endpoint = endpoint['mathalgodb']['sparql']
    )

    dic = {}
    options = []

    # Store results in dict
    for result in results:
        dic.update(
            {
                result['label']['value']: {
                    'id': result['id']['value'],
                    'quote': result['quote']['value']
                }
            }
        )

    # Filter results by user-defined search
    options.extend(
        [
            {
                'id': f"{source}:{value['id']}",
                'text': f'{key} ({value["quote"]}) [{source}]'
            }
            for key, value in dic.items()
            if search.lower() in key.lower()
        ]
    )

    return options

def query_sources_with_user_additions(search, project, setup):
    '''Fetch options from KG, user-defined fields, and other sources.'''

    if setup['sources'] is None:
        setup['sources'] = ['mardi', 'wikidata']

    # Query sources and get the results directly in options
    try:
        options = query_sources(
            search = search,
            query_id = setup['query_id'],
            sources = setup['sources'],
            not_found = False
        )
    except(requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.error("Query sources failed: %s", e)
        options = []

    # Dictionaries for User Answers
    values = {}
    dic = {}

    for query_attribute in setup['query_attributes']:

        # Fetch User entries from the project (ID)
        values['id'] = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f'{BASE_URI}domain/{query_attribute}/id'
            )
        )

        # Fetch User entries from the project (Name)
        values['name'] = project.values.filter(
            snapshot = None,
            attribute=Attribute.objects.get(
                uri = f'{BASE_URI}domain/{query_attribute}/name'
            )
        )

        # Fetch User entries from the project (Description)
        values['description'] = project.values.filter(
            snapshot = None,
            attribute=Attribute.objects.get(
                uri = f'{BASE_URI}domain/{query_attribute}/description'
            )
        )

        # Zip user-defined answers
        zipped = zip(
            values['id'],
            values['name'],
            values['description']
        )

        # Process user-defined answers
        for idx, (value1, value2, value3) in enumerate(zipped):
            item = dict.fromkeys(["source", "label", "description", "id"], None)
            if value1.text:
                if value1.text == 'not found':
                    # User-Defined Cases
                    item['label'] = value2.text or "No Label Provided!"
                    item['description'] = value3.text or "No Description Provided!"
                    item['id'] = idx
                    item['source'] = 'user'
                else:
                    # ID Cases
                    item['label'], item['description'], item['source'] = extract_parts(value1.text)
                    _, item['id'] = value1.external_id.split(':')
            if item['source'] not in setup['sources']:
                if item['source'] == 'user':
                    dic[f"{item['label']} ({item['description']}) [{item['source']}]"] = {
                        'id': "not found"
                    }
                else:
                    dic[f"{item['label']} ({item['description']}) [{item['source']}]"] = {
                        'id': f"{item['source']}:{item['id']}"
                    }

    # Add the user-defined options to the list, filtered by search
    options.extend(
        [
            {
                'id': f"{value['id']}",
                'text': key
            }
            for key, value in dic.items() if search.lower() in key.lower()
        ]
    )

    if setup['creation']:
        options = [{'id': 'not found', 'text': f"{search} [user]"}] + options

    # Return combined, sorted options
    return sorted(options, key=lambda option: option['text'])
