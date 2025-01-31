import html

from ..id import *
from ..config import mardi_endpoint, mardi_wiki
from ..utils import query_sparql
from .sparql import quote_sparql, res_obj_sparql, res_disc_sparql, mmsio_sparql, query_base

def search(answers, options):
    
    # SPARQL via Research Objectives

    quote_str = ''
    res_obj_strs = ''

    # If SPARQL query via research objective desired
    if answers['search'].get('via_research_objective') == options['Yes']:
        quote_str = quote_sparql
        # Separate key words for SPARQL query vie research objective
        if answers['search'].get('research_objective'):
            for res_obj in answers['search']['research_objective'].values():
                # Define Filters for SPARQL queries
                res_obj_strs += res_obj_sparql.format(res_obj.lower())

    # SPARQL via Research Disciplines

    res_disc_str = ''

    # If SPARQL query via research discipline desired
    if answers['search'].get('via_research_discipline') == options['Yes']:
        # Separate disciplines for SPARQL query via research discipline 
        if answers['search'].get('research_discipline'):
            for key in answers['search']['research_discipline'].keys():
                # Get ID and Name of Research Discipline
                ID, Name = answers['search']['research_discipline'][key]['selection'].split(' <|> ') 
                answers['search']['research_discipline'][key].update({'ID': ID})
                answers['search']['research_discipline'][key].update({'Name': Name})
                # Define Filters for SPARQL queries
                res_disc_str += res_disc_sparql.format(P5, ID.split(':')[-1])

    # SPARQL via Mathematical Models, Methods, Softwares, Input or Output Data Sets

    mmsios_str = ''

    # If SPARQL query via Mathematical Models, Methods, Softwares, Input or Output Data Sets
    if answers['search'].get('via_workflow_entity') == options['Yes']:
        # Separate Mathematical Model, Methods, Software, Input or Output Data Sets
        if answers['search'].get('workflow_entity'):
            for key in answers['search']['workflow_entity'].keys():
                # Get ID and Name of Research Discipline
                ID, Name = answers['search']['workflow_entity'][key]['selection'].split(' <|> ') 
                answers['search']['workflow_entity'][key].update({'ID': ID})
                answers['search']['workflow_entity'][key].update({'Name': Name})
                # Define Filters for SPARQL queries
                mmsios_str += mmsio_sparql.format(P6, ID.split(':')[-1])

    # Set up entire SPARQL query
    query = "\n".join(line for line in query_base.format(P4, Q2, res_disc_str, mmsios_str, quote_str, res_obj_strs).splitlines() if line.strip())

    # Add Query to answer dictionary
    answers['query'] = html.escape(query).replace('\n', '<br>')
    
    # Query MaRDI Portal
    results = query_sparql(query, mardi_endpoint)

    # Number of Results
    answers['no_results'] = str(len(results))
    
    # Generate Links to Wikipage and Knowledge Graoh Entry of Results
    links=[]
    for result in results:
        links.append([result["label"]["value"], mardi_wiki + result["label"]["value"].replace(' ','_'), mardi_wiki + 'Item:'+result["qid"]["value"]])

    answers['links'] = links

    return answers

    