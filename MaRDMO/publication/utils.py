'''Module containing Utility Functions for the Publication Documentation'''

import re
from multiprocessing.pool import ThreadPool

import requests

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute

from .models import Author, Journal, Publication

from ..constants import BASE_URI
from ..getters import get_items, get_properties, get_sparql_query, get_url
from ..queries import query_sparql, query_sparql_pool

def additional_queries(publication, choice, key, parameter, function):
    '''Additional MaRDI Portal and Wikidata SPARQL Queries instance like authors or journals'''

    # Get & Extract Information from  Wikidata
    wikidata_query = get_sparql_query(
        f"publication/queries/{key}.sparql"
    ).format(
        *parameter['wikidata']
    )
    wikidata_results = query_sparql(
        wikidata_query,
        get_url('wikidata', 'sparql')
    )
    wikidata_info = function(wikidata_results)

    # Get & Extract Information from MaRDI Portal
    wikidata_id = ' '.join(
        f'"{entity.id}"' if entity.id else '""'
        for entity in wikidata_info.values()
    )

    if wikidata_id:
        parameter['mardi'][-1] = wikidata_id

    mardi_query = get_sparql_query(
        f"publication/queries/{key}.sparql"
    ).format(
        *parameter['mardi']
    )
    mardi_results = query_sparql(
        mardi_query,
        get_url('mardi', 'sparql')
    )
    mardi_info = function(mardi_results)

    # Add (missing) MaRDI Portal / Wikidata IDs to authors
    if mardi_info:
        assign_id(
            getattr(
                publication[choice],
                key
            ),
            mardi_info,
            'mardi'
        )
    elif wikidata_info:
        assign_id(
            getattr(
                publication[choice],
                key
            ),
            wikidata_info,
            'wikidata'
        )

def assign_id(entities, target, prefix):
    '''Function to assign an ID to an entity.'''
    for entity in entities:
        if (
            not entity.id
            or entity.id in ('not found', 'no author found', 'no journal found')
            or entity.id.startswith('wikidata')
        ):
            for id_entity in target.values():
                if entity.label.lower() == id_entity.label.lower():
                    entity.id = f"{prefix}:{id_entity.id}"
                    entity.label = id_entity.label
                    entity.description = id_entity.description

def assign_orcid(publication, source, id_type = 'orcid'):
    '''Funcion to assign an ORCiD to an Author'''
    for author in publication[source].authors:
        if not author.orcid_id:
            for id_author in publication[id_type].values():
                if author.label == id_author.label:
                    author.orcid_id = id_author.orcid_id

def clean_background_data(key_dict, questions, project, snapshot, set_index):
    '''Function to clean data safed in the background'''
    for key in key_dict:
        Value.objects.filter(
            attribute_id = Attribute.objects.get(
                uri = f'{BASE_URI}{questions[key]["uri"]}'
            ),
            set_index = set_index,
            project = project,
            snapshot = snapshot
        ).delete()

def extract_authors(data):
    '''Function to extract Author Information from query results'''
    authors = {}
    if data:
        for idx, entry in enumerate(data[0].get('author_info', {}).get('value', '').split(" | ")):
            if entry:
                authors[idx] = Author.from_query(entry)
    return authors

def extract_journals(data):
    '''Function to extract Journal Information from query results'''
    journals = {}
    if data:
        for idx, entry in enumerate(data[0].get('journal_info', {}).get('value', '').split(" | ")):
            if entry:
                journals[idx] = Journal.from_query(entry)
    return journals

def generate_label(data):
    '''Function to generate a Publication Label for MathAlgoDB'''
    name = year = title = ''
    if data.authors:
        name = data.authors[0].label.split(' ')[-1]
    if data.date:
        year = data.date[:4]
    if data.title:
        title = data.title
    return f'{name} ({year}) {title}'

def get_citation(doi):
    '''Function to get citation information from DOI'''
    publication = {}

    if not re.match(r'10.\d{4,9}/[-._;()/:a-z0-9A-Z]+', doi):
        return publication

    choice = None

    # Define MaRDI Portal / Wikidata / MathAlgoDB SPARQL Queries
    mardi_query = get_sparql_query(
        'publication/queries/full_doi_mardi.sparql'
    ).format(
        doi,
        **get_items(),
        **get_properties()
    )
    wikidata_query = get_sparql_query(
        'publication/queries/full_doi_wikidata.sparql'
    ).format(
        doi
    )
    mathalgodb_query = get_sparql_query(
        'publication/queries/full_doi_mathalgodb.sparql'
    ).format(
        doi
    )

    # Get Citation Data from MaRDI Portal / Wikidata / MathAlgoDB
    results = query_sparql_pool(
        {
            'wikidata': (wikidata_query, get_url('wikidata', 'sparql')),
            'mardi':(mardi_query, get_url('mardi', 'sparql')),
            'mathalgodb':(mathalgodb_query, get_url('mathalgodb', 'sparql'))
        }
    )

    # Structure Publication Information
    for key in ['mardi', 'wikidata', 'mathalgodb']:
        try:
            publication[key] = Publication.from_query(results.get(key))
        except:
            publication[key] = None

    # Return if Publication found on MaRDI
    if publication['mardi']:
        return publication

    if not publication['wikidata']:
        # If no Citation Data in KGs get information from CrossRef, DataCite, DOI, zbMath
        pool = ThreadPool(processes=4)
        results = pool.map(
            lambda fn: fn(doi),
            [
                get_crossref_data,
                get_datacite_data,
                get_zbmath_data,
                get_doi_data
            ]
        )

        for idx, source in enumerate(['crossref', 'datacite', 'zbmath', 'doi']):
            if hasattr(results[idx], "status_code") and results[idx].status_code == 200:
                source_func_name = f"from_{source}"
                source_func = getattr(Publication, source_func_name)
                publication[source] = source_func(results[idx])
            else:
                publication[source] = None

    # Get Authors assigned to publication from ORCID
    publication['orcid'] = {}
    response = get_orcids(doi)
    if response.status_code == 200:
        orcids = response.json().get('result')
        if orcids:
            for idx, entry in enumerate(orcids):
                orcid_id = entry.get('orcid-identifier', {}).get('path', '')
                response = get_author_by_orcid(orcid_id)
                if response.status_code == 200:
                    orcid_author = response.json()
                    publication['orcid'][idx] = Author.from_orcid(orcid_author)

    # Add (missing) ORCID IDs to authors
    for choice in ['mardi', 'wikidata', 'crossref', 'datacite', 'zbmath', 'doi']:
        if publication.get(choice):
            assign_orcid(publication, choice)
            break
    else:
        choice = None

    # Additional Queries for chosen information source
    if choice:
        # Check if Authors already in MaRDI Portal or Wikidata
        orcid_id = ' '.join(
            f'"{author.orcid_id}"' if author.orcid_id else '""'
            for author in publication[choice].authors
        )
        zbmath_id = ' '.join(
            f'"{author.zbmath_id}"' if author.zbmath_id else '""'
            for author in publication[choice].authors
        )
        wikidata_id = ' '.join(
            f'"{author.wikidata_id}"' if author.wikidata_id else '""'
            for author in publication[choice].authors
        )

        properties = get_properties()
        if orcid_id and zbmath_id and wikidata_id:
            additional_queries(
                publication,
                choice,
                'authors', 
                {
                    'mardi': [
                        orcid_id,
                        zbmath_id,
                        properties['ORCID iD'],
                        properties['zbMATH author ID'],
                        properties['Wikidata QID'],
                        wikidata_id
                    ],
                    'wikidata': [
                        orcid_id,
                        zbmath_id,
                        'P496',
                        'P1556',
                        '',
                        wikidata_id
                    ],
                },
                extract_authors
            )

        # Check if Journal already in MaRDI Portal or Wikidata
        journal_id = wikidata_id = ""
        if publication[choice].journal:
            if publication[choice].journal[0].issn:
                journal_id = f'"{publication[choice].journal[0].issn}"'
            if (
                publication[choice].journal[0].id
                and 'wikidata' in publication[choice].journal[0].id
            ):
                wikidata_id = f'"{publication[choice].journal[0].id.split(":")[1]}"'

        if journal_id or wikidata_id:
            additional_queries(
                publication,
                choice,
                'journal',
                {
                    'mardi': [
                        journal_id,
                        properties['ISSN'],
                        properties['Wikidata QID'],
                        wikidata_id
                    ],
                    'wikidata': [
                        journal_id,
                        'P236',
                        '',
                        wikidata_id
                    ],
                },
                extract_journals
            )

    return publication

def get_crossref_data(doi):
    '''Function to get Citation Information from Crossref'''
    try:
        request = requests.get(
            f"https://api.crossref.org/works/{doi}",
            timeout = 5
        )
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as error:
        return error

def get_datacite_data(doi):
    '''Function to get Citation Information from Datacite'''
    try:
        request = requests.get(
            f"https://api.datacite.org/dois/{doi}",
            timeout = 5
        )
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as error:
        return error

def get_doi_data(doi):
    '''Function to get Citation Information from DOI'''
    try:
        request = requests.get(
            f"https://citation.doi.org/metadata?doi={doi}",
            headers = {"accept": "application/json"},
            timeout = 0.0000001
        )
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as error:
        return error

def get_zbmath_data(doi):
    '''Function to get Citation Information from ZbMath'''
    try:
        request = requests.get(
            f"https://api.zbmath.org/v1/document/_structured_search?page=0&results_per_page=100&DOI={doi}",
            timeout = 5
        )
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as error:
        return error

def get_orcids(doi):
    '''Function to get ORCiD Information from ORCiD'''
    try:
        request = requests.get(
            f'https://pub.orcid.org/v3.0/search/?q=doi-self:"{doi}"',
            headers = {'Accept': 'application/json'},
            timeout = 5
        )
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as error:
        return error

def get_author_by_orcid(orcid_id):
    '''Function to get Author Information by ORCiD'''
    try:
        request = requests.get(
            f"https://pub.orcid.org/v3.0/{orcid_id}/personal-details",
            headers = {'Accept': 'application/json'},
            timeout = 5
        )
        request.raise_for_status()
        return request
    except requests.exceptions.RequestException as error:
        return error
