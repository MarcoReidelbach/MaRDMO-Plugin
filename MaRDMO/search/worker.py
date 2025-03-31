import html

from ..config import endpoint
from ..utils import query_sparql
from .sparql import algorithmic_problem_sparql, software_sparql, algorithmic_problem_filter_sparql, quote_sparql, quantity_sparql, task_sparql, formulation_sparql, res_obj_sparql, res_disc_sparql, mmsio_sparql, query_base, query_base_model, query_base_algorithm, problem_sparql, problem_filter_sparql, field_sparql

def search(answers, options):
    
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
                    ID, Name = answers['search']['research_discipline'][key]['selection'].split(' <|> ') 
                    answers['search']['research_discipline'][key].update({'ID': ID})
                    answers['search']['research_discipline'][key].update({'Name': Name})
                    # Define Filters for SPARQL queries
                    res_disc_str += res_disc_sparql.format('437', ID.split(':')[-1])

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
                    mmsios_str += mmsio_sparql.format('557', ID.split(':')[-1])

        # Set up entire SPARQL query
        query = "\n".join(line for line in query_base.format('31', 'Q68657', res_disc_str, mmsios_str, quote_str, res_obj_strs).splitlines() if line.strip())
        
        # Add Query to answer dictionary
        answers['query'] = html.escape(query).replace('\n', '<br>')

        # Query MaRDI Portal
        results = query_sparql(query, endpoint['mardi']['sparql'])

        # Number of Results
        answers['no_results'] = str(len(results))

        # Generate Links to Wikipage and Knowledge Graoh Entry of Results
        links=[]
        for result in results:
            links.append([result["label"]["value"], endpoint['mardi']['uri'] + 'wiki/workflow:' + result["qid"]["value"][1:], endpoint['mardi']['uri'] + 'wiki/Item:' + result["qid"]["value"]])

        answers['links'] = links

    elif answers['search'].get('options') == options['MathematicalModel']:

        # SPARQL via Research Problems

        pro_str = ''
        pro_fil_strs = ''
        
        # If SPARQL query via research objective desired
        if answers['search'].get('via_research_problem') == options['Yes']:
            pro_str = problem_sparql
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
                    ID, Name = answers['search']['research_field'][key]['selection'].split(' <|> ') 
                    answers['search']['research_field'][key].update({'ID': ID})
                    answers['search']['research_field'][key].update({'Name': Name})
                    # Define Filters for SPARQL queries
                    fie_str += field_sparql.format(ID)

        # SPARQL via Mathematical Formulations, Computational Task and Quantities

        for_str = ''
        ta_str = ''
        qu_str = ''
        
        # If SPARQL query via model entity desired
        if answers['search'].get('via_model_entity') == options['Yes']:
            # Via Formulations
            if answers['search'].get('model_formulation'):
                for key in answers['search']['model_formulation'].keys():
                    # Get ID and Name of Formulation
                    ID, Name = answers['search']['model_formulation'][key]['selection'].split(' <|> ') 
                    answers['search']['model_formulation'][key].update({'ID': ID})
                    answers['search']['model_formulation'][key].update({'Name': Name})
                    # Define Filters for SPARQL queries
                    for_str += formulation_sparql.format(ID)
            # Via Computational Tasls
            if answers['search'].get('model_task'):
                for key in answers['search']['model_task'].keys():
                    # Get ID and Name of Computational Task
                    ID, Name = answers['search']['model_task'][key]['selection'].split(' <|> ') 
                    answers['search']['model_task'][key].update({'ID': ID})
                    answers['search']['model_task'][key].update({'Name': Name})
                    # Define Filters for SPARQL queries
                    ta_str += task_sparql.format(ID)
            # Via Computational Tasls
            if answers['search'].get('model_quantity'):
                for key in answers['search']['model_quantity'].keys():
                    # Get ID and Name of Computational Task
                    ID, Name = answers['search']['model_quantity'][key]['selection'].split(' <|> ') 
                    answers['search']['model_quantity'][key].update({'ID': ID})
                    answers['search']['model_quantity'][key].update({'Name': Name})
                    # Define Filters for SPARQL queries
                    qu_str += quantity_sparql.format(ID)

        # Set up entire SPARQL query
        query = "\n".join(line for line in query_base_model.format(pro_str, pro_fil_strs, fie_str, for_str, ta_str, qu_str).splitlines() if line.strip())

        # Add Query to answer dictionary
        answers['query'] = html.escape(query).replace('\n', '<br>')

        # Query MathModDB
        results = query_sparql(query, endpoint['mathmoddb']['sparql'])

        # Number of Results
        answers['no_results'] = str(len(results))

        # Generate Links to Entry
        links=[]
        for result in results:
            links.append([result["label"]["value"], endpoint['mathmoddb']['uri'] + 'object/mathmoddb:' + result["qid"]["value"], ''])

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
                    ID, Name = answers['search']['software'][key]['selection'].split(' <|> ') 
                    answers['search']['software'][key].update({'ID': ID})
                    answers['search']['software'][key].update({'Name': Name})
                    # Define Filters for SPARQL queries
                    sof_str += software_sparql.format(f"software:{ID.split(':')[1]}")

        # Set up entire SPARQL query
        query = "\n".join(line for line in query_base_algorithm.format(apr_str, apr_fil_strs, sof_str).splitlines() if line.strip())
        
        # Add Query to answer dictionary
        answers['query'] = html.escape(query).replace('\n', '<br>')

        # Query MathAlgoDB
        results = query_sparql(query, endpoint['mathalgodb']['sparql'])

        # Number of Results
        answers['no_results'] = str(len(results))

        # Generate Links to Entry
        links=[]
        for result in results:
            links.append([result["label"]["value"], endpoint['mathalgodb']['uri'] + 'object/al:' + result["qid"]["value"], ''])

        answers['links'] = links

    return answers

    
