import re
import requests

from multiprocessing.pool import ThreadPool

from .models import Author, Journal, Publication
from .sparql import queryPublication

from ..config import endpoint
from ..getters import get_items, get_properties
from ..queries import query_sparql_pool

def additional_queries(publication, choice, key, mardi_parameter, wikidata_parameter, function):
    '''Additional MaRDI Portal and Wikidata SPARQL Queries instance like authors or journals'''
    mardi_query = queryPublication[key].format(*mardi_parameter)
    wikidata_query = queryPublication[key].format(*wikidata_parameter)
    # Get Journal Information from MaRDI Portal / Wikidata
    results = query_sparql_pool({'wikidata':(wikidata_query, endpoint['wikidata']['sparql']), 'mardi':(mardi_query, endpoint['mardi']['sparql'])})
    mardi_info = function(results['mardi'])
    wikidata_info = function(results['wikidata'])
    # Add (missing) MaRDI Portal / Wikidata IDs to authors
    assign_id(getattr(publication[choice],key), mardi_info, 'mardi')
    assign_id(getattr(publication[choice],key), wikidata_info, 'wikidata')
    return

def assign_id(entities, target, prefix):
    for entity in entities:
        if not entity.id or entity.id == 'not found' or entity.id == 'no author found':
            for id_entity in target.values():
                if entity.label.lower() == id_entity.label.lower():
                    entity.id = f"{prefix}:{id_entity.id}"
                    entity.label = id_entity.label
                    entity.description = id_entity.description
    return

def assign_orcid(publication, source, id='orcid'):
    for author in publication[source].authors:
        if not author.orcid_id:
            for id_author in publication[id].values():
                if author.label == id_author.label:
                    author.orcid_id = id_author.orcid_id
    return

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

    publication = {}
    if re.match(r'10.\d{4,9}/[-._;()/:a-z0-9A-Z]+', DOI):
        
        choice = None

        # Define MaRDI Portal / Wikidata / MathModDB / MathAlgoDB SPARQL Queries
        mardi_query = queryPublication['MaRDI']['DOI_FULL'].format(DOI, **get_items(), **get_properties())
        wikidata_query = queryPublication['Wikidata']['DOI_FULL'].format(DOI)
        mathalgodb_query = queryPublication['PublicationMathAlgoDBDOI'].format(DOI)
        
        # Get Citation Data from MaRDI Portal / Wikidata / MathAlgoDB
        results = query_sparql_pool({'wikidata':(wikidata_query, endpoint['wikidata']['sparql-scholarly']), 
                                     'mardi':(mardi_query, endpoint['mardi']['sparql']),  
                                     'mathalgodb':(mathalgodb_query, endpoint['mathalgodb']['sparql'])})

        # Structure Publication Information            
        for key in ['mardi', 'wikidata', 'mathalgodb']:
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
                properties = get_properties()
                if orcid_id and zbmath_id:
                    additional_queries(publication, choice, 'authors', 
                                       [orcid_id, zbmath_id, properties['ORCID iD'], properties['zbMATH author ID'], properties['Wikidata QID']], 
                                       [orcid_id, zbmath_id, 'P496', 'P1556', ''], 
                                       extract_authors)
                # Check if Journal already in MaRDI Portal or Wikidata
                journal_id = publication[choice].journal[0].issn
                if journal_id:
                    additional_queries(publication, choice, 'journal', 
                                       [journal_id, properties['ISSN']], 
                                       [journal_id, 'P236'], 
                                       extract_journals)
        
    return publication

def get_crossref_data(doi):
    return requests.get(f"{endpoint['crossref']['api']}{doi}")

def get_datacite_data(doi):
    return requests.get(f"{endpoint['datacite']['api']}{doi}")

def get_doi_data(doi):
    return requests.get(f"{endpoint['doi']['api']}{doi}", headers={"accept": "application/json"})

def get_zbmath_data(doi):
    return requests.get(f"{endpoint['zbmath']['api']}{doi}")

def get_orcids(doi):
    return requests.get(f"{endpoint['orcid']['api']}/search/?q=doi-self:{doi}", headers={'Accept': 'application/json'})

def get_author_by_orcid(orcid_id):
    return requests.get(f"{endpoint['orcid']['api']}/{orcid_id}/personal-details", headers={'Accept': 'application/json'})

