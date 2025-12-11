'''Worker Module to search Models, Workflows, and Algorithms'''

import html

from ..getters import get_item_url, get_items, get_properties, get_url
from ..queries import query_sparql
from .sparql import (
    algorithmic_problem_sparql,
    software_sparql,
    algorithmic_problem_filter_sparql,
    quote_sparql,
    quantity_sparql,
    quantity_filter_sparql,
    task_sparql,
    formulation_sparql,
    res_obj_sparql,
    res_disc_sparql,
    mmsio_sparql,
    query_base,
    query_base_model,
    query_base_algorithm,
    problem_sparql,
    problem_filter_sparql,
    field_sparql
)

def search(answers, options):
    '''Function to build queries, get results and add to answers'''
    if answers['search'].get('options') == options['InterdisciplinaryWorkflow']:

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
                    identifier = answers['search']['research_discipline'][key]['ID'].split(':')[1]
                    name = answers['search']['research_discipline'][key]['Name']
                    answers['search']['research_discipline'][key].update({'ID': identifier})
                    answers['search']['research_discipline'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    res_disc_str += res_disc_sparql.format(
                        identifier.split(':')[-1],
                        **get_items(),
                        **get_properties()
                    )

        # SPARQL via Mathematical Models, Methods, Softwares, Input or Output Data Sets

        mmsios_str = ''

        # If SPARQL query via Mathematical Models, Methods, Softwares, Input or Output Data Sets
        if answers['search'].get('via_workflow_entity') == options['Yes']:
            # Separate Mathematical Model, Methods, Software, Input or Output Data Sets
            if answers['search'].get('workflow_entity'):
                for key in answers['search']['workflow_entity'].keys():
                    # Get ID and Name of Research Discipline
                    identifier = answers['search']['workflow_entity'][key]['ID'].split(':')[1]
                    name = answers['search']['workflow_entity'][key]['Name']
                    answers['search']['workflow_entity'][key].update({'ID': identifier})
                    answers['search']['workflow_entity'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    mmsios_str += mmsio_sparql.format(
                        identifier.split(':')[-1],
                        **get_items(),
                        **get_properties()
                    )

        # Set up entire SPARQL query
        query = "\n".join(
            line
            for line in query_base.format(
                res_disc_str,
                mmsios_str,
                quote_str,
                res_obj_strs,
                **get_items(),
                **get_properties(),
            ).splitlines()
            if line.strip()
        )

        # Add Query to answer dictionary
        answers['query'] = html.escape(query).replace('\n', '<br>')

        # Query MaRDI Portal
        results = query_sparql(query, get_url('mardi', 'sparql'))

        # Number of Results
        answers['no_results'] = str(len(results))

        # Generate Links to Wikipage and Knowledge Graoh Entry of Results
        links=[]
        for result in results:
            links.append(
                [
                    result["label"]["value"],
                    f"{get_url('mardi', 'uri')}/wiki/workflow:{result['qid']['value'][1:]}",
                    f"{get_item_url('mardi')}{result['qid']['value']}"
                ]
            )

        answers['links'] = links

    elif answers['search'].get('options') == options['MathematicalModel']:

        # SPARQL via Research Problems

        pro_str = ''
        pro_fil_strs = ''

        # If SPARQL query via research objective desired
        if answers['search'].get('via_research_problem') == options['Yes']:
            pro_str = problem_sparql.format(**get_items(), **get_properties())
            # Separate key words for SPARQL query vie research objective
            if answers['search'].get('research_problem'):
                for res_pro in answers['search']['research_problem'].values():
                    # Define Filters for SPARQL queries
                    pro_fil_strs += problem_filter_sparql.format(res_pro.lower())

        # SPARQL via Research Fields

        fie_str = ''

        # If SPARQL query via research field desired
        if answers['search'].get('via_research_field') == options['Yes']:
            #fie_str = field_sparql
            # Separate key words for SPARQL query vie research objective
            if answers['search'].get('research_field'):
                for key in answers['search']['research_field'].keys():
                    # Get ID and Name of Research Field
                    identifier = answers['search']['research_field'][key]['ID'].split(':')[1]
                    name = answers['search']['research_field'][key]['Name']
                    answers['search']['research_field'][key].update({'ID': identifier})
                    answers['search']['research_field'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    fie_str += field_sparql.format(
                        identifier,
                        **get_items(),
                        **get_properties()
                    )

        # SPARQL via Mathematical Formulations, Computational Task and Quantities

        for_str = ''
        ta_str = ''
        qu_str = quantity_sparql.format(**get_items(), **get_properties())

        # If SPARQL query via model entity desired
        if answers['search'].get('via_model_entity') == options['Yes']:
            # Via Formulations
            if answers['search'].get('model_formulation'):
                for key in answers['search']['model_formulation'].keys():
                    # Get ID and Name of Formulation
                    identifier = answers['search']['model_formulation'][key]['ID'].split(':')[1]
                    name = answers['search']['model_formulation'][key]['Name']
                    answers['search']['model_formulation'][key].update({'ID': identifier})
                    answers['search']['model_formulation'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    for_str += formulation_sparql.format(
                        identifier,
                        **get_items(),
                        **get_properties()
                    )
            # Via Computational Tasls
            if answers['search'].get('model_task'):
                for key in answers['search']['model_task'].keys():
                    # Get ID and Name of Computational Task
                    identifier = answers['search']['model_task'][key]['ID'].split(':')[1]
                    name = answers['search']['model_task'][key]['Name']
                    answers['search']['model_task'][key].update({'ID': identifier})
                    answers['search']['model_task'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    ta_str += task_sparql.format(
                        identifier,
                        **get_items(),
                        **get_properties()
                    )
            # Via Computational Tasls
            if answers['search'].get('model_quantity'):
                for idx, key in enumerate(answers['search']['model_quantity'].keys()):
                    # Get ID and Name of Computational Task
                    identifier = answers['search']['model_quantity'][key]['ID'].split(':')[1]
                    name = answers['search']['model_quantity'][key]['Name']
                    answers['search']['model_quantity'][key].update({'ID': identifier})
                    answers['search']['model_quantity'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    if idx == 0:
                        qu_str += quantity_filter_sparql.format(
                            identifier,
                            **get_items(),
                            **get_properties()
                        )
                    else:
                        qu_str += """\n UNION""" + quantity_filter_sparql.format(
                            identifier,
                            **get_items(),
                            **get_properties()
                        )

        # Set up entire SPARQL query
        query = "\n".join(
            line
            for line in query_base_model.format(
                pro_str,
                pro_fil_strs,
                fie_str,
                for_str,
                ta_str,
                qu_str,
                **get_items(),
                **get_properties()
            ).splitlines()
            if line.strip()
        )

        # Add Query to answer dictionary
        answers['query'] = html.escape(query).replace('\n', '<br>')

        # Query MathModDB
        results = query_sparql(query, get_url('mardi', 'sparql'))

        # Number of Results
        answers['no_results'] = str(len(results))

        # Generate Links to Entry
        links=[]
        for result in results:
            links.append(
                [
                    result["label"]["value"],
                    f"{get_url('mardi', 'uri')}/wiki/model:{result['qid']['value'][1:]}",
                    f"{get_item_url('mardi')}{result['qid']['value']}"
                ]
            )

        answers['links'] = links

    elif answers['search'].get('options') == options['Algorithm']:

        # SPARQL via Algorithmic Problems

        apr_str = ''
        apr_fil_strs = ''

        # If SPARQL query via research objective desired
        if answers['search'].get('via_algorithmic_problem') == options['Yes']:
            apr_str = algorithmic_problem_sparql
            # Separate key words for SPARQL query vie research objective
            if answers['search'].get('algorithmic_problem'):
                for alg_pro in answers['search']['algorithmic_problem'].values():
                    # Define Filters for SPARQL queries
                    apr_fil_strs += algorithmic_problem_filter_sparql.format(alg_pro.lower())

        # SPARQL via Softwares

        sof_str = ''

        # If SPARQL query via software desired
        if answers['search'].get('via_software') == options['Yes']:
            # Separate key words for SPARQL query vie research objective
            if answers['search'].get('software'):
                for key in answers['search']['software'].keys():
                    # Get ID and Name of Software
                    identifier = answers['search']['software'][key]['ID'].split(':')[1]
                    name = answers['search']['software'][key]['Name']
                    answers['search']['software'][key].update({'ID': identifier})
                    answers['search']['software'][key].update({'Name': name})
                    # Define Filters for SPARQL queries
                    sof_str += software_sparql.format(f"software:{identifier}")

        # Set up entire SPARQL query
        query = "\n".join(
            line
            for line in query_base_algorithm.format(
                apr_str,
                apr_fil_strs,
                sof_str
            ).splitlines()
            if line.strip()
        )

        # Add Query to answer dictionary
        answers['query'] = html.escape(query).replace('\n', '<br>')

        # Query MathAlgoDB
        results = query_sparql(query, get_url('mathalgodb', 'sparql'))

        # Number of Results
        answers['no_results'] = str(len(results))

        # Generate Links to Entry
        links=[]
        for result in results:
            links.append(
                [
                    result["label"]["value"],
                    get_url('mathalgodb', 'uri') + 'object/al:' + result["qid"]["value"],
                    ''
                ]
            )

        answers['links'] = links

    return answers
