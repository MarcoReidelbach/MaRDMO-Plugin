'''Function that query Data'''

import requests
import logging

from multiprocessing.pool import ThreadPool
from rdmo.domain.models import Attribute

from .algorithm.sparql import queryProviderAL
from .config import BASE_URI, endpoint
from .helpers import extract_parts

logger = logging.getLogger(__name__)

def query_item(label, description, api=endpoint['mardi']['api']):
    '''API request returning an Item whose label or alias matches, and with matching description.'''
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
        if (item_label == norm_label or norm_label in item_aliases) and item_description == description:
            matched_items.append(item)

    if matched_items:
        return matched_items[0]['id']
    else:
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
            headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'},
            timeout=timeout
        )
        response.raise_for_status()  # Raise an error on bad HTTP status codes
        try:
            return response.json().get('search', [])
        except ValueError:
            # Malformed JSON
            logger.error("Failed to parse JSON.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed due to {e}")

    return []

def query_sparql(query, endpoint):
    '''SPARQL request returning all Items with matching properties.'''
    if not endpoint:
        logger.warning("SPARQL query attempted without a valid endpoint.")
        return []
    
    try:
        response = requests.post(
            endpoint,
            data=query,
            headers={
                "Content-Type": "application/sparql-query",
                "Accept": "application/sparql-results+json"
            }
        )
        # Check if request was successful
        if response.status_code == 200:
            return response.json().get('results', {}).get('bindings', [])
        else:
            logger.error(f"SPARQL request to {endpoint} failed with status {response.status_code}: {response.text}")
            return []

    except requests.exceptions.ConnectionError:
        logger.error(f"SPARQL query failed: Unable to connect to the {endpoint}.")
    except requests.exceptions.RequestException as e:
        logger.exception(f"SPARQL request failed: {e}")
    
    return []

def query_sparql_pool(input):
    '''Pooled SPARQL request returning all items with matching properties from different endpoints'''
    pool = ThreadPool(processes=len(input))
    # Map each endpoint's query and store results in a dictionary
    data = {key: result for key, result in zip(input.keys(), pool.map(lambda args: query_sparql(*args), input.values()))}
    return data

def query_sources(search, queryID = '', sources = ['mardi', 'wikidata'], notFound=True):
        '''Helper function to query specified sources and process results.'''
        
        def process_result(result, source):
            '''Function to process the result and return a dictionary with id and text'''
            return {
                 'id': f"{source}:{result['id']}",
                 'text': f"{result['display']['label']['value']} ({result['display'].get('description', {}).get('value', 'No Description Provided!')}) [{source}]"
            }
        
        source_functions = {
            'wikidata': lambda s: query_api(endpoint['wikidata']['api'], s),
            'mardi': lambda s: query_api(endpoint['mardi']['api'], s),
            'mathalgodb': lambda s: query_provider(s, queryProviderAL[queryID], 'mathalgodb')
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

        if notFound:
            options = [{'id': 'not found', 'text': 'not found'}] + options
        return options

def query_provider(search, query, source):
    """
    Dynamic query of MathModDB and MathAlgoDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathAlgoDB knowledge graph
    results = query_sparql(query, endpoint['mathalgodb']['sparql'] if source == 'mathalgodb' else endpoint['mathmoddb']['sparql'] if source == 'mathmoddb' else '')
    dic = {}
    options = []
    
    # Store results in dict
    for result in results:
        dic.update({result['label']['value']:{'id':result['id']['value'], 'quote':result['quote']['value']}})

    # Filter results by user-defined search
    options.extend([{'id': f"{source}:{dic[key]['id']}", 'text': f'{key} ({dic[key]["quote"]}) [{source}]'} for key in dic if search.lower() in key.lower()])

    return options

def query_sources_with_user_additions(search, project, queryAttributes, creation = False, queryID = '', sources = ['mardi', 'wikidata']):
    '''Fetch options from MathModDB, user-defined fields, and other sources.'''
    # Query sources and get the results directly in options
    try:
        options = query_sources(search, queryID, sources, False)
    except:
        options = []

    # Dictionary for User Answers
    dic = {}

    for queryAttribute in queryAttributes:
        # Fetch user-defined research fields from the project
        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/id'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/name'))
        values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/description'))

        # Process user-defined answers
        for idx, (value1, value2, value3) in enumerate(zip(values1, values2, values3)):
            source = label = description = None
            if value1.text:
                if value1.text == 'not found':
                    # User-Defined Cases
                    label = value2.text or "No Label Provided!"
                    description = value3.text or "No Description Provided!"
                    id = idx
                    source = 'user'
                else:
                    # ID Cases
                    label, description, source = extract_parts(value1.text)
                    _, id = value1.external_id.split(':')
            if source not in sources:
                if source == 'user':
                    dic[f"{label} ({description}) [{source}]"] = {'id': f"not found"}
                else:
                    dic[f"{label} ({description}) [{source}]"] = {'id': f"{source}:{id}"}
            
    # Add the user-defined options to the list, filtered by search
    options.extend([{'id': f"{dic[key]['id']}", 'text': key} for key in dic if search.lower() in key.lower()])
    
    if creation:
        options = [{'id': 'not found', 'text': f"{search} [user]"}] + options

    # Return combined, sorted options
    return sorted(options, key=lambda option: option['text'])