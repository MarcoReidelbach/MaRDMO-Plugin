from dataclasses import asdict

from .sparql import queryPreview
from .models import ModelProperties, Variables, Parameters
from .constants import REPRODUCIBILITY

from ..utils import find_item, get_options, unique_items, query_sparql, GeneratePayload
from ..id_staging import ITEMS, PROPERTIES
from ..config import endpoint

class prepareWorkflow:

    def preview(data):

        # Update Model Properties via MathModDB
        if data.get('model',{}).get('ID'):
            _, id = data['model']['ID'].split(':')
            query = queryPreview['basic'].format(id, **ITEMS, **PROPERTIES)
            basic = query_sparql(query, endpoint['mardi']['sparql'])
            if basic:
                data.get('model', {}).update(asdict(ModelProperties.from_query(basic)))
        
        # Update Model Variables and Parameters via MathModDB
        if data.get('specifictask'):            
            query = queryPreview['variables'].format(' '.join(f"wd:{value.get('ID', '').split(':')[1]}" for _, value in data['specifictask'].items()), **ITEMS, **PROPERTIES)
            variables = query_sparql(query, endpoint['mardi']['sparql'])
            if variables:
                for idx, variable in enumerate(variables):
                    data.setdefault('variables', {}).update({idx: asdict(Variables.from_query(variable))})
            query = queryPreview['parameters'].format(' '.join(f"wd:{value.get('ID', '').split(':')[1]}" for _, value in data['specifictask'].items()), **ITEMS, **PROPERTIES)
            parameters = query_sparql(query, endpoint['mardi']['sparql'])
            if parameters:
                for idx, parameter in enumerate(parameters):
                    data.setdefault('parameters', {}).update({idx: asdict(Parameters.from_query(parameter))})

        return data

    def export(data, title, url):

        items = unique_items(data, title)
        
        payload = GeneratePayload(url, items)

        # Load Options
        options = get_options()

        # Add / Retrieve Components of Interdisciplinary Workflow Item
        for key, value in items.items():
            if value.get('ID'):
                # Item from MaRDI Portal
                if 'mardi:' in value['ID']:
                    _, id = value['ID'].split(':')
                    payload.add_entry('dictionary', key, payload.build_item(id, value['Name'], value['Description']))
                # Item from Wikidata
                elif 'wikidata:' in value['ID']:
                    _, id = value['ID'].split(':')
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description'], [[PROPERTIES['Wikidata QID'], 'external-id', id]]))
                # Item from MathAlgoDB KG
                elif 'mathalgodb' in value['ID']:
                    _, id = value['ID'].split(':')
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description']))
                        # No MathAlgoDB ID Property in Portal yet
                # Item defined by User (I)
                elif 'not found' in value['ID']:
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        statement = []
                        if value.get('ISSN'):
                            statement = statement.extend([[PROPERTIES['ISSN'], 'external-id', value['ISSN']]])
                        payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description'], statement))
                # Item defined by User (II)
                elif 'no author found' in value['ID']:
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        statement = []
                        if value.get('orcid'):
                            statement = statement.extend([[PROPERTIES['ORCID iD'], 'external-id', value['orcid']]])
                        if value.get('zbmath'):
                            statement = statement.extend([[PROPERTIES['zbMATH author ID'], 'external-id', value['zbmath']]])
                        if statement:
                            payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description'], statement))

        
        ### Add additional Algorithms / Methods Information
        for method in data.get('method', {}).values():

            # Continue if no ID exists
            if not method.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(method)

            # Add Class
            if 'mathalgodb' in method['ID']:
                payload.add_answer(PROPERTIES['instance of'], ITEMS['algorithm'])
            else:
                payload.add_answer(PROPERTIES['instance of'], ITEMS['method'])
        
        ### Add additional Software Information
        for software in data.get('software', {}).values():

            # Continue if no ID exists
            if not software.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(software)

            # Add Class
            payload.add_answer(PROPERTIES['instance of'], ITEMS['software'])

            # Add References of the Software
            for reference in software.get('Reference', {}).values():
                if reference[0] == options['DOI']:
                    payload.add_answer(PROPERTIES['DOI'], reference[1], 'external-id')
                elif reference[0] == options['SWMATH']:
                    payload.add_answer(PROPERTIES['swMath work ID'], reference[1], 'external-id')
                elif reference[0] == options['URL']:
                    payload.add_answer(PROPERTIES['URL'], reference[1], 'url')

            # Add Programming Languages
            payload.add_forward_relation_single(PROPERTIES['programmed in'], 'programminglanguage')

            # Add Dependencies
            payload.add_forward_relation_single(PROPERTIES['depends on software'], 'dependency')

            # Add Source Code Repository
            if software.get('Published', [''])[0] == options['YesText']:
                payload.add_answer(PROPERTIES['source code repository URL'], software['Published'][1], 'url')
                
            # Add Documentation / Manual
            if software.get('Documented', [''])[0] == options['YesText']:
                payload.add_answer(PROPERTIES['user manual URL'], software['Documented'][1], 'url')

        ### Add additional Hardware Information
        for hardware in data.get('hardware', {}).values():

            # Continue if no ID exists
            if not hardware.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(hardware)

            # Add Class
            payload.add_answer(PROPERTIES['instance of'], ITEMS['computer hardware'])

            # Add CPU
            payload.add_forward_relation_single(PROPERTIES['CPU'], 'cpu')

            # Add Number of Computing Nodes
            if hardware['Nodes']:
                payload.add_answer(predicate = PROPERTIES['has part(s)'], 
                                   object = ITEMS['compute node'],
                                   qualifier = [{"property":{"id":PROPERTIES['quantity_property']},"value":{"type":"value","content":{"amount":f"+{hardware['Nodes']}","unit":"1"}}}]
                                   )

            # Add Number of Processor Cores
            if hardware['Cores']:
                payload.add_answer(predicate = PROPERTIES['number of processor cores'], 
                                   object = {"amount":f"+{hardware['Cores']}","unit":"1"},
                                   object_type = 'quantity'
                                   ) 

        ### Add additional Instrument Information
        for instrument in data.get('instrument', {}).values():

            # Continue if no ID exists
            if not instrument.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(instrument)

            # Add Class
            payload.add_answer(PROPERTIES['instance of'], ITEMS['research tool'])

            ### MORE INSTRUMENT INFORMATION TO ADD ###

        ### Add additional Dataset Information
        for dataset in data.get('dataset', {}).values():

            # Continue if no ID exists
            if not dataset.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(dataset)

            # Add Class
            payload.add_answer(PROPERTIES['instance of'], ITEMS['data set'])

            # Size of the data set
            if dataset.get('Size'):
                if dataset['Size'][0] == options['kilobyte']:
                    predicate = PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{ITEMS['kilobyte']}"}
                elif dataset['Size'][0] == options['megabyte']:
                    predicate = PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{ITEMS['megabyte']}"}
                elif dataset['Size'][0] == options['gigabyte']:
                    predicate = PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{ITEMS['gigabyte']}"}
                elif dataset['Size'][0] == options['terabyte']:
                    predicate = PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{ITEMS['terabyte']}"}
                elif dataset['Size'][0] == options['items']:
                    predicate = PROPERTIES['number of records']
                    object = {"amount":f"+{dataset['Size'][1]}","unit":"1"}
                payload.add_answer(predicate, object, 'quantity')
                
            # Add Data Type 
            payload.add_forward_relation_single(relation = PROPERTIES['uses'], 
                                                relatant = 'datatype', 
                                                qualifier = payload.add_qualifier(PROPERTIES['object has role'], 'wikibase-item', ITEMS['data type']))

            # Add Representation Format 
            payload.add_forward_relation_single(relation = PROPERTIES['uses'], 
                                                relatant = 'representationformat', 
                                                qualifier = payload.add_qualifier(PROPERTIES['object has role'], 'wikibase-item', ITEMS['representation format']))            

            # Add File Format
            if dataset.get('FileFormat'):
                payload.add_answer(PROPERTIES['file extension'], dataset['FileFormat'], 'string') 

            # Add binary or text data
            if dataset.get('BinaryText'):
                if dataset['BinaryText'] == options['binary']:
                    payload.add_answer(PROPERTIES['instance of'], ITEMS['binary data'])
                elif dataset['BinaryText'] == options['text']:
                    payload.add_answer(PROPERTIES['instance of'], ITEMS['text data'])

            # Data Set Proprietary
            if dataset.get('Proprietary'):
                if dataset['Proprietary'] == options['Yes']:
                    payload.add_answer(PROPERTIES['instance of'], ITEMS['proprietary information'])
                elif dataset['Proprietary'] == options['No']:
                    payload.add_answer(PROPERTIES['instance of'], ITEMS['open data'])

            # Data Set to Publish
            if dataset.get('ToPublish'):
                if dataset['ToPublish'].get(0, ['',''])[0] == options['Yes']:
                    payload.add_answer(PROPERTIES['mandates'], ITEMS['data publishing'])
                    if dataset['ToPublish'].get(1, ['',''])[0] == options['DOI']:
                        payload.add_answer(PROPERTIES['DOI'], dataset['ToPublish'][1][1], 'external-id')
                    if dataset['ToPublish'].get(2, ['',''])[0] == options['URL']:
                        payload.add_answer(PROPERTIES['URL'], dataset['ToPublish'][2][1], 'url')
                        
            # Data Set To Archive
            if dataset.get('ToArchive'):
                if dataset['ToArchive'][0] == options['YesText']:
                    qualifier = []
                    if dataset['ToArchive'][1]:
                        qualifier = payload.add_qualifier(PROPERTIES['end time'], 'time', {"time":f"+{dataset['ToArchive'][1]}-00-00T00:00:00Z","precision":9,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"})
                    payload.add_answer(PROPERTIES['mandates'], ITEMS['research data archiving'], 'wikibase-item', qualifier)
                    
        ### Add Process Step Information
        for processstep in data.get('processstep', {}).values():

            # Continue if no ID exists
            if not processstep.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(processstep)

            # Add Class
            payload.add_answer(PROPERTIES['instance of'], ITEMS['process step'])

            # Add Input Data Sets
            payload.add_forward_relation_single(PROPERTIES['input data set'], 'input')

            # Add Output Data Sets
            payload.add_forward_relation_single(PROPERTIES['output data set'], 'output')

            # Add applied Methods
            for method in processstep.get('method', {}).values():
                # Continue if no ID exists
                if not method.get('ID'):
                    continue
                # Get Entry Key
                method_item = payload.get_item_key(method, 'object')
                # Get Qualifier
                qualifier = []
                for parameter in method.get('Parameter', {}).values():
                    qualifier.extend(payload.add_qualifier(PROPERTIES['comment'], 'string', parameter))
                # Add to Payload
                payload.add_answer(PROPERTIES['uses'], method_item, 'wikibase-item', qualifier)

            # Add Software Environment
            payload.add_forward_relation_single(relation = PROPERTIES['platform'], 
                                                relatant = 'environmentSoftware',
                                                qualifier = payload.add_qualifier(PROPERTIES['object has role'], 'wikibase-item', ITEMS['software']))
            
            # Add Instrument Environment
            payload.add_forward_relation_single(relation = PROPERTIES['platform'], 
                                                relatant = 'environmentInstrument',
                                                qualifier = payload.add_qualifier(PROPERTIES['object has role'], 'wikibase-item', ITEMS['research tool']))
            
            # Add Disciplines (math and non-math)
            for discipline in processstep.get('discipline', {}).values():
                # Check if new ID exists
                if 'msc:' in discipline.get('ID'):
                    _, id = discipline['ID'].split(':')
                    payload.add_answer(PROPERTIES['MSC ID'], id, 'external-id')
                else:
                    # Get Discipline Key
                    discipline_item = payload.get_item_key(discipline, 'object')
                    # Add to Payload
                    payload.add_answer(PROPERTIES['field of work'], discipline_item)

        # Add Publication Information
        for publication in data.get('publication', {}).values():

            # Continue if no ID exists
            if not publication.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(publication)

            if 'mardi' not in publication['ID'] and 'wikidata' not in publication['ID']:
                # Add the class of the Publication
                if publication.get('entrytype'):
                    payload.add_answer(PROPERTIES['instance of'], ITEMS['scholarly article'] if publication['entrytype'] == 'scholarly article' else ITEMS['publication'])
                # Add the Title of the Publication
                if publication.get('title'):
                    payload.add_answer(PROPERTIES['title'], {"text": publication['title'], "language": "en"}, 'monolingualtext')
                # Add the Volume of the Publication
                if publication.get('volume'):
                    payload.add_answer(PROPERTIES['volume'], publication['volume'], 'string')
                # Add the Issue of the Publication
                if publication.get('issue'):
                    payload.add_answer(PROPERTIES['issue'], publication['issue'], 'string')
                # Add the Page(s) of the Publication
                if publication.get('page'):
                    payload.add_answer(PROPERTIES['page(s)'], publication['page'], 'string')
                # Add the Date of the Publication
                if publication.get('date'):
                    payload.add_answer(PROPERTIES['publication date'], {"time":f"+{publication['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}, 'time')
                # Add the DOI of the Publication
                if publication.get('reference', {}).get(0):
                    payload.add_answer(PROPERTIES['DOI'], publication['reference'][0][1], 'external-id')
                
                # Add the Language of the Publication
                payload.add_forward_relation_single(PROPERTIES['language of work or name'], 'language')
                # Add the Journal of the Publication
                payload.add_forward_relation_single(PROPERTIES['published in'], 'journal')
                # Add the Authors of the Publication
                payload.add_forward_relation_single(PROPERTIES['author'], 'author', PROPERTIES['author name string'], 'Name')
        
        # Add Interdisciplinary Workflow Information
        workflow = {'ID': 'not found', 'Name': title, 'Description': data.get('general', {}).get('objective')}
        
        # Get Item Key
        payload.get_item_key(workflow)

        # Add Class
        payload.add_answer(PROPERTIES['instance of'], ITEMS['research workflow'])

        # Procedure Description to Workflow
        if data.get('general', {}).get('procedure'):
           payload.add_answer(PROPERTIES['description'], data['general']['procedure'], 'string')

        # Add Reproducibility Aspects
        for key, value in REPRODUCIBILITY.items():
            if data.get('reproducibility', {}).get(key) == options['Yes']:
                qualifier = []
                if data['reproducibility'].get(f'{key}condition'):
                    qualifier.extend(payload.add_qualifier(PROPERTIES['comment'], 'string', data['reproducibility'][f'{key}condition']))
                payload.add_answer(PROPERTIES['instance of'], ITEMS[value], 'wikibase-item', qualifier)
        
        # Add Transferability Aspects
        if data.get('reproducibility', {}).get('transferability'):
            qualifier = []
            for value in data['reproducibility']['transferability'].values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['comment'], 'string', value))
            payload.add_answer(PROPERTIES['instance of'], ITEMS['transferable research workflow'], 'wikibase-item', qualifier)
        
        # Add Model and Task the Workflow Uses
        for value in data.get('model', {}).values():
            #Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            model_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for task in data.get('specifictask', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['used by'], 'wikibase-item', payload.get_item_key(task, 'object')))
            payload.add_answer(PROPERTIES['uses'], model_item, 'wikibase-item', qualifier)

        # Add Methods the Workflow Uses
        for value in data.get('method', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            method_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for parameter in value.get('Parameter', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['comment'], 'string', parameter))
            for software in value.get('software', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['implemented by'], payload.get_item_key(software, 'object')))
            for instrument in value.get('instrument', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['implemented by'], payload.get_item_key(instrument, 'object')))
            payload.add_answer(PROPERTIES['uses'], method_item, 'wikibase-item', qualifier)

        # Add Software the Workflow uses
        for value in data.get('software', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            software_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for hardware in data.get('hardware', {}).values():
                for software in hardware.get('software', {}).values():
                    if (software.get('ID'), software.get('Name'), software.get('Description')) == (value['ID'], value['Name'], value['Description']):
                        hardware_item = payload.get_item_key(hardware, 'object')
                        qualifier.extend(payload.add_qualifier(PROPERTIES['platform'], 'wikibase-item', hardware_item))
            if value.get('Version'):
                qualifier = payload.add_qualifier(PROPERTIES['software version identifier'], 'string', value['Version'])
            payload.add_answer(PROPERTIES['uses'], software_item, 'wikibase-item', qualifier)
            
        # Add Hardware the Workflow Uses
        for value in data.get('hardware', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            hardware_item = payload.get_item_key(value, 'object')
            # Add Satement with Qualifier
            qualifier = []
            for compiler in value.get('compiler', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['uses'], 'wikibase-item', payload.get_item_key(compiler, 'object')))
            payload.add_answer(PROPERTIES['uses'], hardware_item, 'wikibase-item', qualifier)
            
        # Add instruments the workflow Uses
        for value in data.get('instrument', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            instrument_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifer
            qualifier = []
            if value.get('Version'):
                qualifier.extend(payload.add_qualifier(PROPERTIES['edition number'], 'string', value['Version'])) 
            if value.get('SerialNumber'):
                qualifier.extend(payload.add_qualifier(PROPERTIES['serial number'], 'string', value['SerialNumber'])) 
            for location in value.get('location', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['location'], 'wikibase-item', payload.get_item_key(location, 'object'))) 
            for software in value.get('software', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['uses'], 'wikibase-item', payload.get_item_key(software, 'object'))) 
            payload.add_answer(PROPERTIES['uses'], instrument_item, 'wikibase-item', qualifier)
            
        # Add Data Sets the Workflow Uses
        for value in data.get('dataset', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            dataset_item = payload.get_item_key(value, 'object')
            # Add Statement
            payload.add_answer(PROPERTIES['uses'], dataset_item)

        # Add Process Steps the Workflow Uses
        for value in data.get('processstep', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            processstep_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for parameter in value.get('parameter', {}).values():
                qualifier.extend(payload.add_qualifier(PROPERTIES['comment'], 'string', parameter)) 
            payload.add_answer(PROPERTIES['uses'], processstep_item, 'wikibase-item', qualifier)

        # Add Publications related to the Workflow
        for value in data.get('publication', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            publication_item = payload.get_item_key(value, 'object')
            # Add Statement
            payload.add_answer(PROPERTIES['cites work'], publication_item)

        # Construct Item Payloads
        payload.add_item_payload()
            
        return payload.get_dictionary('dictionary')
