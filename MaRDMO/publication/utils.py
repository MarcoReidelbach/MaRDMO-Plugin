import re
import requests

from multiprocessing.pool import ThreadPool

from rdmo.options.models import Option

from .models import Author, Journal, Publication
from .sparql import queryPublication

from ..id import *
from ..config import BASE_URI, crossref_api, datacite_api, doi_api, mardi_endpoint, mathmoddb_endpoint, mathalgodb_endpoint, wikidata_endpoint, wd, wdt
from ..utils import query_sparql_pool, value_editor

def additional_queries(publication, choice, key, mardi_parameter, wikidata_parameter, function):
    '''Additional MaRDI Portal and Wikidata SPARQL Queries instance like authors or journals'''
    mardi_query = queryPublication[key].format(*mardi_parameter)
    wikidata_query = queryPublication[key].format(*wikidata_parameter)
    # Get Journal Information from MaRDI Portal / Wikidata
    results = query_sparql_pool({'wikidata':(wikidata_query, wikidata_endpoint), 'mardi':(mardi_query, mardi_endpoint)})
    mardi_info = function(results['mardi'])
    wikidata_info = function(results['wikidata'])
    # Add (missing) MaRDI Portal / Wikidata IDs to authors
    assign_id(getattr(publication[choice],key), mardi_info, 'mardi')
    assign_id(getattr(publication[choice],key), wikidata_info, 'wikidata')

def assign_id(entities, target, prefix):
    for entity in entities:
        if not entity.id:
            for id_entity in target.values():
                if entity.label == id_entity.label:
                    entity.id = f"{prefix}:{id_entity.id}"
                    entity.label = id_entity.label
                    entity.description = id_entity.description

def assign_orcid(publication, source, id='orcid'):
    for author in publication[source].authors:
        if not author.orcid_id:
            for id_author in publication[id].values():
                if author.label == id_author.label:
                    author.orcid_id = id_author.orcid_id

def extract_authors(data):
    authors = {}
    if data:
        for idx, entry in enumerate(data[0].get('authorInfos', {}).get('value', '').split(" | ")):
            if entry:
                authors[idx] = Author.from_query(entry)
    return authors

def extract_journals(data):
    journals = {}
    if data:
        for idx, entry in enumerate(data[0].get('journalInfos', {}).get('value', '').split(" | ")):
            if entry:
                journals[idx] = Journal.from_query(entry)
    return journals

def generate_label(data):
    name = year = title = ''
    if data.authors:
        name = data.authors[0].label.split(' ')[-1]
    if data.date:
        year = data.date[:4]
    if data.title:
        title = data.title
    return f'{name} ({year}) {title}'

def get_citation(DOI):

    if re.match(r'10.\d{4,9}/[-._;()/:a-z0-9A-Z]+', DOI):
        
        choice = None

        # Define MaRDI Portal / Wikidata / MathModDB / MathAlgoDB SPARQL Queries
        mardi_query = queryPublication['All_MaRDI'].format(P16, DOI.upper(), P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23, wdt, wd)
        wikidata_query = queryPublication['All_Wikidata'].format('356', DOI.upper(), '50', '496', '31', '1433', '407', '1476', '2093', '577', '478', '433', '304', '', '1556')
        mathmoddb_query = queryPublication['PublicationMathModDBDOI'].format(DOI)
        mathalgodb_query = queryPublication['PublicationMathAlgoDBDOI'].format(DOI)
        
        # Get Citation Data from MaRDI Portal / Wikidata / MathModDB / MathAlgoDB
        results = query_sparql_pool({'wikidata':(wikidata_query, wikidata_endpoint), 'mardi':(mardi_query, mardi_endpoint), 'mathmoddb':(mathmoddb_query, mathmoddb_endpoint), 'mathalgodb':(mathalgodb_query, mathalgodb_endpoint)})

        # Structure Publication Information            
        publication = {}
        for key in ['mardi', 'wikidata', 'mathmoddb', 'mathalgodb']:
            try:
                publication[key] = Publication.from_query(results.get(key))
            except:
                publication[key] = None

        if not (publication['mardi'] or publication['wikidata']):

            # If no Citation Data in KGs and additional sources requested by User, get Citation Information from CrossRef, DataCite, DOI, zbMath 
            pool = ThreadPool(processes=4)
            results = pool.map(lambda fn: fn(DOI), [get_crossref_data, get_datacite_data, get_doi_data, get_zbmath_data])
            
            for idx, source in enumerate(['crossref', 'datacite', 'doi', 'zbmath']):
                try:
                    source_func_name = f"from_{source}"
                    source_func = getattr(Publication, source_func_name)
                    publication[source] = source_func(results[idx])
                except:
                    publication[source] = None      
            # Get Authors assigned to publication from ORCID
            publication['orcid'] = {}
            response = get_orcids(DOI)
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
            for choice in ['zbmath', 'crossref', 'datacite', 'doi']:
                if publication[choice]:
                    assign_orcid(publication, choice)
                    break
            else:
                choice = None

            # Additional for chosen information source
            if choice:
                # Check if Authors already in MaRDI Portal or Wikidata
                orcid_id = ' '.join(f'"{author.orcid_id}"' if author.orcid_id else '""' for author in publication[choice].authors)
                zbmath_id = ' '.join(f'"{author.zbmath_id}"' if author.zbmath_id else '""' for author in publication[choice].authors)
                if orcid_id and zbmath_id:
                    additional_queries(publication, choice, 'authors', [orcid_id, zbmath_id, P22, P23, P2], [orcid_id, zbmath_id, '496', '1556', ''], extract_authors)
                # Check if Journal already in MaRDI Portal or Wikidata
                journal_id = publication[choice].journal[0].issn
                if journal_id:
                    additional_queries(publication, choice, 'journal', [journal_id, P33], [journal_id, '236'], extract_journals)
    
    return publication

def get_crossref_data(doi):
    return requests.get(f'{crossref_api}{doi}')

def get_datacite_data(doi):
    return requests.get(f'{datacite_api}{doi}')

def get_doi_data(doi):
    return requests.get(f'{doi_api}{doi}', headers={"accept": "application/json"})

def get_zbmath_data(doi):
    return requests.get(f'https://api.zbmath.org/v1/document/_structured_search?page=0&results_per_page=100&external%20id={doi}')

def get_orcids(doi):
    return requests.get(f'https://pub.orcid.org/v3.0/search/?q=doi-self:{doi}', headers={'Accept': 'application/json'})

def get_author_by_orcid(orcid_id):
    return requests.get(f'https://pub.orcid.org/v3.0/{orcid_id}/personal-details', headers={'Accept': 'application/json'})

