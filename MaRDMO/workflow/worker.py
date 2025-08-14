from dataclasses import asdict

from .sparql import queryPreview
from .models import ModelProperties, Variables, Parameters
from .constants import REPRODUCIBILITY

from ..config import endpoint
from ..getters import get_items, get_options, get_properties
from ..helpers import unique_items
from ..queries import query_item, query_sparql
from ..payload import GeneratePayload

class prepareWorkflow:

    def __init__(self):
        self.ITEMS = get_items()
        self.PROPERTIES = get_properties()

    def preview(self, data):

        # Update Model Properties via MathModDB
        if data.get('model',{}).get('ID'):
            _, id = data['model']['ID'].split(':')
            query = queryPreview['basic'].format(id, **self.ITEMS, **self.PROPERTIES)
            basic = query_sparql(query, endpoint['mardi']['sparql'])
            if basic:
                data.get('model', {}).update(asdict(ModelProperties.from_query(basic)))
        
        # Update Model Variables and Parameters via MathModDB
        if data.get('model', {}).get('task'):            
            query = queryPreview['variables'].format(' '.join(f"wd:{value.get('ID', '').split(':')[1]}" for _, value in data['model']['task'].items()), **self.ITEMS, **self.PROPERTIES)
            variables = query_sparql(query, endpoint['mardi']['sparql'])
            if variables:
                for idx, variable in enumerate(variables):
                    data.setdefault('variables', {}).update({idx: asdict(Variables.from_query(variable))})
            query = queryPreview['parameters'].format(' '.join(f"wd:{value.get('ID', '').split(':')[1]}" for _, value in data['model']['task'].items()), **self.ITEMS, **self.PROPERTIES)
            parameters = query_sparql(query, endpoint['mardi']['sparql'])
            if parameters:
                for idx, parameter in enumerate(parameters):
                    data.setdefault('parameters', {}).update({idx: asdict(Parameters.from_query(parameter))})

        return data

    def export(self,data, title, url):

        items = unique_items(data, title)
        
        payload = GeneratePayload(url, items)

        # Load Options
        options = get_options()

        # Add / Retrieve Components of Interdisciplinary Workflow Item
        payload.process_items()
        
        ### Add additional Algorithms / Methods Information
        for method in data.get('method', {}).values():

            # Continue if no ID exists
            if not method.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(method)

            # Add Class
            if 'mathalgodb' in method['ID']:
                payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['algorithm'])
            else:
                payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['method'])
        
        ### Add additional Software Information
        for software in data.get('software', {}).values():

            # Continue if no ID exists
            if not software.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(software)

            # Add Class
            payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['software'])

            # Add References of the Software
            for reference in software.get('Reference', {}).values():
                if reference[0] == options['DOI']:
                    payload.add_answer(self.PROPERTIES['DOI'], reference[1], 'external-id')
                elif reference[0] == options['SWMATH']:
                    payload.add_answer(self.PROPERTIES['swMath work ID'], reference[1], 'external-id')
                elif reference[0] == options['URL']:
                    payload.add_answer(self.PROPERTIES['URL'], reference[1], 'url')

            # Add Programming Languages
            payload.add_forward_relation_single(self.PROPERTIES['programmed in'], 'programminglanguage')

            # Add Dependencies
            payload.add_forward_relation_single(self.PROPERTIES['depends on software'], 'dependency')

            # Add Source Code Repository
            if software.get('Published', [''])[0] == options['YesText']:
                payload.add_answer(self.PROPERTIES['source code repository URL'], software['Published'][1], 'url')
                
            # Add Documentation / Manual
            if software.get('Documented', [''])[0] == options['YesText']:
                payload.add_answer(self.PROPERTIES['user manual URL'], software['Documented'][1], 'url')

        ### Add additional Hardware Information
        for hardware in data.get('hardware', {}).values():

            # Continue if no ID exists
            if not hardware.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(hardware)

            # Add Class
            payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['computer hardware'])

            # Add CPU
            payload.add_forward_relation_single(self.PROPERTIES['CPU'], 'cpu')

            # Add Number of Computing Nodes
            if hardware['Nodes']:
                payload.add_answer(predicate = self.PROPERTIES['has part(s)'], 
                                   object = self.ITEMS['compute node'],
                                   qualifier = [{"property":{"id":self.PROPERTIES['quantity_property']},"value":{"type":"value","content":{"amount":f"+{hardware['Nodes']}","unit":"1"}}}]
                                   )

            # Add Number of Processor Cores
            if hardware['Cores']:
                payload.add_answer(predicate = self.PROPERTIES['number of processor cores'], 
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
            payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['research tool'])

            ### MORE INSTRUMENT INFORMATION TO ADD ###

        ### Add additional Dataset Information
        for dataset in data.get('dataset', {}).values():

            # Continue if no ID exists
            if not dataset.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(dataset)

            # Add Class
            payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['data set'])

            # Size of the data set
            if dataset.get('Size'):
                if dataset['Size'][0] == options['kilobyte']:
                    predicate = self.PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{self.ITEMS['kilobyte']}"}
                elif dataset['Size'][0] == options['megabyte']:
                    predicate = self.PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{self.ITEMS['megabyte']}"}
                elif dataset['Size'][0] == options['gigabyte']:
                    predicate = self.PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{self.ITEMS['gigabyte']}"}
                elif dataset['Size'][0] == options['terabyte']:
                    predicate = self.PROPERTIES['data size']
                    object = {"amount":f"+{dataset['Size'][1]}","unit": f"{endpoint['mardi']['uri']}/entity/{self.ITEMS['terabyte']}"}
                elif dataset['Size'][0] == options['items']:
                    predicate = self.PROPERTIES['number of records']
                    object = {"amount":f"+{dataset['Size'][1]}","unit":"1"}
                payload.add_answer(predicate, object, 'quantity')
                
            # Add Data Type 
            payload.add_forward_relation_single(relation = self.PROPERTIES['uses'], 
                                                relatant = 'datatype', 
                                                qualifier = payload.add_qualifier(self.PROPERTIES['object has role'], 'wikibase-item', self.ITEMS['data type']))

            # Add Representation Format 
            payload.add_forward_relation_single(relation = self.PROPERTIES['uses'], 
                                                relatant = 'representationformat', 
                                                qualifier = payload.add_qualifier(self.PROPERTIES['object has role'], 'wikibase-item', self.ITEMS['representation format']))            

            # Add File Format
            if dataset.get('FileFormat'):
                payload.add_answer(self.PROPERTIES['file extension'], dataset['FileFormat'], 'string') 

            # Add binary or text data
            if dataset.get('BinaryText'):
                if dataset['BinaryText'] == options['binary']:
                    payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['binary data'])
                elif dataset['BinaryText'] == options['text']:
                    payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['text data'])

            # Data Set Proprietary
            if dataset.get('Proprietary'):
                if dataset['Proprietary'] == options['Yes']:
                    payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['proprietary information'])
                elif dataset['Proprietary'] == options['No']:
                    payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['open data'])

            # Data Set to Publish
            if dataset.get('ToPublish'):
                if dataset['ToPublish'].get(0, ['',''])[0] == options['Yes']:
                    payload.add_answer(self.PROPERTIES['mandates'], self.ITEMS['data publishing'])
                    if dataset['ToPublish'].get(1, ['',''])[0] == options['DOI']:
                        payload.add_answer(self.PROPERTIES['DOI'], dataset['ToPublish'][1][1], 'external-id')
                    if dataset['ToPublish'].get(2, ['',''])[0] == options['URL']:
                        payload.add_answer(self.PROPERTIES['URL'], dataset['ToPublish'][2][1], 'url')
                        
            # Data Set To Archive
            if dataset.get('ToArchive'):
                if dataset['ToArchive'][0] == options['YesText']:
                    qualifier = []
                    if dataset['ToArchive'][1]:
                        qualifier = payload.add_qualifier(self.PROPERTIES['end time'], 'time', {"time":f"+{dataset['ToArchive'][1]}-00-00T00:00:00Z","precision":9,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"})
                    payload.add_answer(self.PROPERTIES['mandates'], self.ITEMS['research data archiving'], 'wikibase-item', qualifier)
                    
        ### Add Process Step Information
        for processstep in data.get('processstep', {}).values():

            # Continue if no ID exists
            if not processstep.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(processstep)

            # Add Class
            payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['process step'])

            # Add Input Data Sets
            payload.add_forward_relation_single(self.PROPERTIES['input data set'], 'input')

            # Add Output Data Sets
            payload.add_forward_relation_single(self.PROPERTIES['output data set'], 'output')

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
                    qualifier.extend(payload.add_qualifier(self.PROPERTIES['comment'], 'string', parameter))
                # Add to Payload
                payload.add_answer(self.PROPERTIES['uses'], method_item, 'wikibase-item', qualifier)

            # Add Software Environment
            payload.add_forward_relation_single(relation = self.PROPERTIES['platform'], 
                                                relatant = 'environmentSoftware',
                                                qualifier = payload.add_qualifier(self.PROPERTIES['object has role'], 'wikibase-item', self.ITEMS['software']))
            
            # Add Instrument Environment
            payload.add_forward_relation_single(relation = self.PROPERTIES['platform'], 
                                                relatant = 'environmentInstrument',
                                                qualifier = payload.add_qualifier(self.PROPERTIES['object has role'], 'wikibase-item', self.ITEMS['research tool']))
            
            # Add Disciplines (math and non-math)
            for discipline in processstep.get('discipline', {}).values():
                # Check if new ID exists
                if 'msc:' in discipline.get('ID'):
                    _, id = discipline['ID'].split(':')
                    payload.add_answer(self.PROPERTIES['MSC ID'], id, 'external-id')
                else:
                    # Get Discipline Key
                    discipline_item = payload.get_item_key(discipline, 'object')
                    # Add to Payload
                    payload.add_answer(self.PROPERTIES['field of work'], discipline_item)

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
                    payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['scholarly article'] if publication['entrytype'] == 'scholarly article' else self.ITEMS['publication'])
                # Add the Title of the Publication
                if publication.get('title'):
                    payload.add_answer(self.PROPERTIES['title'], {"text": publication['title'], "language": "en"}, 'monolingualtext')
                # Add the Volume of the Publication
                if publication.get('volume'):
                    payload.add_answer(self.PROPERTIES['volume'], publication['volume'], 'string')
                # Add the Issue of the Publication
                if publication.get('issue'):
                    payload.add_answer(self.PROPERTIES['issue'], publication['issue'], 'string')
                # Add the Page(s) of the Publication
                if publication.get('page'):
                    payload.add_answer(self.PROPERTIES['page(s)'], publication['page'], 'string')
                # Add the Date of the Publication
                if publication.get('date'):
                    payload.add_answer(self.PROPERTIES['publication date'], {"time":f"+{publication['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}, 'time')
                # Add the DOI of the Publication
                if publication.get('reference', {}).get(0):
                    payload.add_answer(self.PROPERTIES['DOI'], publication['reference'][0][1], 'external-id')
                
                # Add the Language of the Publication
                payload.add_forward_relation_single(self.PROPERTIES['language of work or name'], 'language')
                # Add the Journal of the Publication
                payload.add_forward_relation_single(self.PROPERTIES['published in'], 'journal')
                # Add the Authors of the Publication
                payload.add_forward_relation_single(self.PROPERTIES['author'], 'author', self.PROPERTIES['author name string'], 'Name')
        
        # Add Interdisciplinary Workflow Information
        workflow = {'ID': 'not found', 'Name': title, 'Description': data.get('general', {}).get('objective')}
        
        # Get Item Key
        payload.get_item_key(workflow)

        # Add Class
        payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['research workflow'])

        # Procedure Description to Workflow
        if data.get('general', {}).get('procedure'):
           payload.add_answer(self.PROPERTIES['description'], data['general']['procedure'], 'string')

        # Add Reproducibility Aspects
        for key, value in REPRODUCIBILITY.items():
            if data.get('reproducibility', {}).get(key) == options['Yes']:
                qualifier = []
                if data['reproducibility'].get(f'{key}condition'):
                    qualifier.extend(payload.add_qualifier(self.PROPERTIES['comment'], 'string', data['reproducibility'][f'{key}condition']))
                payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS[value], 'wikibase-item', qualifier)
        
        # Add Transferability Aspects
        if data.get('reproducibility', {}).get('transferability'):
            qualifier = []
            for value in data['reproducibility']['transferability'].values():
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['comment'], 'string', value))
            payload.add_answer(self.PROPERTIES['instance of'], self.ITEMS['transferable research workflow'], 'wikibase-item', qualifier)
        
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
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['used by'], 'wikibase-item', payload.get_item_key(task, 'object')))
            payload.add_answer(self.PROPERTIES['uses'], model_item, 'wikibase-item', qualifier)

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
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['comment'], 'string', parameter))
            for software in value.get('software', {}).values():
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['implemented by'], payload.get_item_key(software, 'object')))
            for instrument in value.get('instrument', {}).values():
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['implemented by'], payload.get_item_key(instrument, 'object')))
            payload.add_answer(self.PROPERTIES['uses'], method_item, 'wikibase-item', qualifier)

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
                        qualifier.extend(payload.add_qualifier(self.PROPERTIES['platform'], 'wikibase-item', hardware_item))
            if value.get('Version'):
                qualifier = payload.add_qualifier(self.PROPERTIES['software version identifier'], 'string', value['Version'])
            payload.add_answer(self.PROPERTIES['uses'], software_item, 'wikibase-item', qualifier)
            
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
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['uses'], 'wikibase-item', payload.get_item_key(compiler, 'object')))
            payload.add_answer(self.PROPERTIES['uses'], hardware_item, 'wikibase-item', qualifier)
            
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
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['edition number'], 'string', value['Version'])) 
            if value.get('SerialNumber'):
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['serial number'], 'string', value['SerialNumber'])) 
            for location in value.get('location', {}).values():
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['location'], 'wikibase-item', payload.get_item_key(location, 'object'))) 
            for software in value.get('software', {}).values():
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['uses'], 'wikibase-item', payload.get_item_key(software, 'object'))) 
            payload.add_answer(self.PROPERTIES['uses'], instrument_item, 'wikibase-item', qualifier)
            
        # Add Data Sets the Workflow Uses
        for value in data.get('dataset', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            dataset_item = payload.get_item_key(value, 'object')
            # Add Statement
            payload.add_answer(self.PROPERTIES['uses'], dataset_item)

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
                qualifier.extend(payload.add_qualifier(self.PROPERTIES['comment'], 'string', parameter)) 
            payload.add_answer(self.PROPERTIES['uses'], processstep_item, 'wikibase-item', qualifier)

        # Add Publications related to the Workflow
        for value in data.get('publication', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            publication_item = payload.get_item_key(value, 'object')
            # Add Statement
            payload.add_answer(self.PROPERTIES['cites work'], publication_item)

        # Construct Item Payloads
        payload.add_item_payload()

        # If Relations are added, check if they exist
        if any(key.startswith('RELATION') for key in payload.get_dictionary('dictionary')):

            # Generate SPARQL Check Query
            query = payload.build_relation_check_query()
        
            # Perform Check Query for Relations
            check = query_sparql(query, endpoint['mardi']['sparql'])

            # Add Check Results
            payload.add_check_results(check)
            
        return payload.get_dictionary('dictionary')
