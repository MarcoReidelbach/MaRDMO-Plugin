from ..utils import find_item, get_data


def generate_payload(data, title):

    # Load Options
    options = get_data('data/options.json')

    # Create an empty Payload Dictionary
    payload = {}
    old_new = {}
    rel_idx = 0
     
    items = unique_items(data, title)
    
    # Add / Retrieve Components of Interdisciplinary Workflow Item

    for key, value in items.items():
        if value.get('ID'):
            # Item from MaRDI Portal
            if 'mardi:' in value['ID']:
                _, id = value['ID'].split(':')
                payload.update({key:{'id': id, 'url': items_uri(), 'payload': ''}})
            # Item from Wikidata
            elif 'wikidata:' in value['ID']:
                _, id = value['ID'].split(':')
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_uri(), 'payload': ''}})
                else:
                    payload.update({key:{'id': '', 'url': items_uri(), 'payload': items_payload(value['Name'], value['Description'])}})
                    payload, rel_idx = add_static_or_non_item_relation(payload, key, rel_idx, 'P2', id, 'external-id')
            # Item from MathModDB KG
            elif 'mathmoddb:' in value['ID']:
                _, id = value['ID'].split(':')
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_uri(), 'payload': ''}})
                else:
                    payload.update({key:{'id': '', 'url': items_uri(), 'payload': items_payload(value['Name'], value['Description'])}})
                    # No MathModDB ID Property in Portal yet
            # Item from MathAlgoDB KG
            elif 'mathalgodb' in value['ID']:
                _, id = value['ID'].split(':')
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_uri(), 'payload': ''}})
                else:
                    payload.update({key:{'id': '', 'url': items_uri(), 'payload': items_payload(value['Name'], value['Description'])}})
                    # No MathAlgoDB ID Property in Portal yet
            # Item defined by User (I)
            elif 'not found' in value['ID']:
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_uri(), 'payload': ''}})
                else:
                    payload.update({key:{'id': '', 'url': items_uri(), 'payload': items_payload(value['Name'], value['Description'])}})
                    if value.get('ISSN'):
                        payload, rel_idx = add_static_or_non_item_relation(payload, key, rel_idx, 'P915', value['ISSN'], 'external-id')
            # Item defined by User (II)
            elif 'no author found' in value['ID']:
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_uri(), 'payload': ''}})
                else:
                    if value.get('orcid') or value.get('zbmath'):
                        payload.update({key:{'id': '', 'url': items_uri(), 'payload': items_payload(value['Name'], value['Description'])}})
                        if value.get('orcid'):
                            payload, rel_idx = add_static_or_non_item_relation(payload, key, rel_idx, 'P33', value['orcid'], 'external-id')
                        if value.get('zbmath'):
                            payload, rel_idx = add_static_or_non_item_relation(payload, key, rel_idx, 'P369', value['zbmath'], 'external-id')

    ### Add additional Algorithms / Methods Information
    for value in data.get('method').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        if 'mathalgodb' in value['ID']:
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q4629')
        else:
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q2822')

    ### Add additional Software Information
    for value in data.get('software').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q420')
        
        # Add References of the Software
        for reference in value.get('Reference', {}).values():
            if reference[0] == options['DOI']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P27', reference[1], 'external-id')
            elif reference[0] == options['SWMATH']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P31', reference[1], 'external-id')
            elif reference[0] == options['URL']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P107', reference[1], 'url')
        
        # Add Programming Languages
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('programminglanguage', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P30')
        
        # Add Dependencies
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('dependency', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P474')
        
        # Add Source Code Repository
        if value.get('Published', [''])[0] == options['YesText']:
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P69', value['Published'][1], 'url')
            
        # Add Documentation / Manual
        if value.get('Documented', [''])[0] == options['YesText']:
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P56', value['Documented'][1], 'url')
            
    ### Add additional Hardware Information
    for value in data.get('hardware').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q387')
        
        # Add CPU
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('cpu', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P585')
        
        # Add Number of Nodes (Computing Nodes)
        if value.get('Nodes'):
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P124', 'Q13129', 'wikibase-item', [{"property":{"id":"P302"},"value":{"type":"value","content":{"amount":f"+{value['Nodes']}","unit":"1"}}}])
            
        # Add Number of Cores (Processor Cores)
        if value.get('Cores'):
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P588', {"amount":f"+{value['Cores']}","unit":"1"}, 'quantity')
            
    ### Add additional Instrument Information
    for value in data.get('instrument').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q4682')
        
    ### Add additional Data Set Information
    for value in data.get('dataset').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q381')
        
        # Size of the data set
        if value.get('Size'):
            if value['Size'][0] == options['kilobyte']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13145"}, 'quantity')
            elif value['Size'][0] == options['megabyte']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13146"}, 'quantity')
            elif value['Size'][0] == options['gigabyte']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13147"}, 'quantity')
            elif value['Size'][0] == options['terabyte']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13148"}, 'quantity')
            elif value['Size'][0] == options['items']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P328', {"amount":f"+{value['Size'][1]}","unit":"1"}, 'quantity')
                
        # Data Type of the data set
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('datatype', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P7',
                                             qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q1917"}}])
        
        # Representation Format of the data set
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('representationformat', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P7',
                                             qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q13149"}}])
        
        # File Format of the Data Set
        if value.get('FileFormat'):
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P792', value['FileFormat'], 'string')
            
        # Data Set binary or text
        if value.get('BinaryText'):
            if value['BinaryText'] == options['binary']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q3742')
            elif value['BinaryText'] == options['text']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13150')
                
        # Data Set Proprietary
        if value.get('Proprietary'):
            if value['Proprietary'] == options['Yes']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q3747')
            elif value['Proprietary'] == options['No']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q3745')
                
        # Data Set To Publish
        if value.get('ToPublish'):
            if value['ToPublish'].get(0, ['',''])[0] == options['Yes']:
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P794', 'Q3743')
                if value['ToPublish'].get(1, ['',''])[0] == options['DOI']:
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P27', value['ToPublish'][1][1], 'external-id')
                if value['ToPublish'].get(2, ['',''])[0] == options['URL']:
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P107', value['ToPublish'][2][1], 'url')
        
        # Data Set To Archive
        if value.get('ToArchive'):
            if value['ToArchive'][0] == options['YesText']:
                qualifier = []
                if value['ToArchive'][1]:
                    qualifier = [{"property":{"id":"P791", 'data_type': 'time'},"value":{"type":"value","content":{"time":f"+{value['ToArchive'][1]}-00-00T00:00:00Z","precision":9,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}}}]
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P794', 'Q3748', 'wikibase-item', qualifier)
                
    ### Add additional Process Step Information
    for value in data.get('processstep').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        # Add the class of the Process Step
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13152')
        
        # Add Input Data Sets
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('input', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P1093')
        
        # Add Output Data Sets
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('output', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P1094')
        
        # Add applied Methods
        for entry in value.get('method', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            qualifier = []
            for parameter in entry.get('Parameter').values():
                qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": parameter}}])
            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', entry_item, 'wikibase-item', qualifier)
            
        # Add Software Environment
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('environmentSoftware', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P402',
                                             qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q420"}}])
        
        # Add Instrument Environment
        payload, rel_idx = add_item_relation(payload = payload, 
                                             values = value.get('environmentInstrument', {}).values(), 
                                             lookup = old_new, 
                                             items = items, 
                                             item = item, 
                                             idx = rel_idx, 
                                             property = 'P402',
                                             qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q4682"}}])
        
        # Add Disciplines (math and non-math)
        for discipline in value.get('discipline', {}).values():
            # Check if new ID exists
            if 'msc:' in discipline.get('ID'):
                _, id = discipline['ID'].split(':')
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P349', id, 'external-id')
            else:
                # Use new ID if exists
                discipline['ID'] = old_new.get((discipline['ID'], discipline['Name'], discipline['Description']), [''])[0] or discipline['ID']
                # Get Item Key
                discipline_item = find_key_by_values(items, discipline['ID'], discipline['Name'], discipline['Description'])
                payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P19', discipline_item)
                
    # Add additional Paper Information
    for value in data.get('publication').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        
        if value.get('workflow') == options['Yes']:
            if 'mardi' not in value['ID'] and 'wikidata' not in value['ID']:
                # Add the class of the Publication
                if value.get('entrytype'):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q259' if value['entrytype'] == 'scholarly article' else 'Q428')
                # Add the Title of the Publication
                if value.get('title'):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P15', {"text": value['title'], "language": "en"}, 'monolingualtext')
                # Add the Volume of the Publication
                if value.get('volume'):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P24', value['volume'], 'string')
                # Add the Issue of the Publication
                if value.get('issue'):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P25', value['issue'], 'string')
                # Add the Page(s) of the Publication
                if value.get('page'):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P26', value['page'], 'string')
                # Add the Date of the Publication
                if value.get('date'):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P22', {"time":f"+{value['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}, 'time')
                # Add the DOI of the Publication
                if value.get('reference', {}).get(0):
                    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P27', value['reference'][0][1], 'external-id')
                
                # Add the Language of the Publication
                payload, rel_idx = add_item_relation(payload = payload, 
                                                     values = value.get('language', {}).values(), 
                                                     lookup = old_new, 
                                                     items = items, 
                                                     item = item, 
                                                     idx = rel_idx, 
                                                     property = 'P6')
                # Add the Journal of the Publication
                payload, rel_idx = add_item_relation(payload = payload, 
                                                     values = value.get('journal', {}).values(), 
                                                     lookup = old_new, 
                                                     items = items, 
                                                     item = item, 
                                                     idx = rel_idx, 
                                                     property = 'P23')
                # Add the Authors of the Publication
                for entry in value.get('author', {}).values():
                    # Continue if no ID exists
                    if not entry.get('ID'):
                        continue
                    # Use new ID if present
                    entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
                    # Get Item Key and add to Payload
                    entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
                    if entry_item in payload.keys():
                        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P20', entry_item)
                    else:
                        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P21', entry['Name'], 'string')
                        
    # Add Interdisciplinary Workflow Information
    if ('not found', title, data.get('general', {}).get('objective')) in old_new.keys():
        workflow_id = old_new[('not found', title, data.get('general', {}).get('objective'))][0]
    else:
        workflow_id = 'not found'

    item = find_key_by_values(items, workflow_id, title, data.get('general', {}).get('objective'))
    
    # Add instance of research workflow
    payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q18')
    
    # Add description to the Workflow
    if data.get('general', {}).get('procedure'):
       payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P896', data['general']['procedure'])
       
    # Add Reproducibility Aspects
    if data.get('reproducibility', {}).get('mathematical') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('mathematicalcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['mathematicalcondition']}}])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13160', 'wikibase-item', qualifier)
        
    if data.get('reproducibility', {}).get('runtime') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('runtimecondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['runtimecondition']}}])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13162', 'wikibase-item', qualifier)

    if data.get('reproducibility', {}).get('result') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('resultcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['resultcondition']}}])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13163', 'wikibase-item', qualifier)
        
    if data.get('reproducibility', {}).get('originalplatform') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('originalplatformcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['originalplatformcondition']}}])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13164', 'wikibase-item', qualifier)
        
    if data.get('reproducibility', {}).get('otherplatform') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('otherplatformcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['otherplatformcondition']}}])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13165', 'wikibase-item', qualifier)
        
    if data.get('reproducibility', {}).get('transferability'):
        qualifier = []
        for value in data['reproducibility']['transferability'].values():
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": value}}])
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P3', 'Q13166', 'wikibase-item', qualifier)
        
    # Add methods the workflow uses
    for value in data.get('method').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Method Key
        method_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier_strings = []
        for parameter in value.get('Parameter').values():
            qualifier_strings.append(parameter)
        
        qualifier_items = []
        for software in value.get('software', {}).values():
            # Use new ID if present
            software['ID'] = old_new.get((software['ID'], software['Name'], software['Description']), [''])[0] or software['ID']
            # Get Software Keys and add to Qualifier
            qualifier_items.append(find_key_by_values(items, software['ID'], software['Name'], software['Description']))
        
        for instrument in value.get('instrument', {}).values():
            # Use new ID if present
            instrument['ID'] = old_new.get((instrument['ID'], instrument['Name'], instrument['Description']), [''])[0] or instrument['ID']
            # Get Instrument Key and add to Qualifier
            qualifier_items.append(find_key_by_values(items, instrument['ID'], instrument['Name'], instrument['Description']))
        
        qualifier = []
        for qualifier_item in qualifier_items:
            qualifier.extend([{"property": {"id": "P1089"},"value": {"type": "value","content": qualifier_item}}])

        for qualifier_string in qualifier_strings:
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": qualifier_string}}])

        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', method_item, 'wikibase-item', qualifier)
        
    # Add software the workflow uses
    for value in data.get('software').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Software Key
        software_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier = []
        for hardware in data.get('hardware').values():
            for software in hardware.get('software').values():
                if software.get('ID') == value['ID'] and software.get('Name') == value['Name'] and software.get('Description') == value['Description']:
                    hardware_item = find_key_by_values(items, hardware['ID'], hardware['Name'], hardware['Description'])
                    qualifier.extend([{"property": {"id": "P402"},"value": {"type": "value","content": hardware_item}}])
        
        if value.get('Version'):
            qualifier = [{"property": {"id": "P472"},"value": {"type": "value","content": value['Version']}}]
            
        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', software_item, 'wikibase-item', qualifier)
        
    # Add hardware the workflow uses
    for value in data.get('hardware').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        if value.get('ID'):
            hardware_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

            qualifier_items = []
            for compiler in value.get('compiler', {}).values():
                # Use new ID if present
                compiler['ID'] = old_new.get((compiler['ID'], compiler['Name'], compiler['Description']), [''])[0] or compiler['ID']
                # Get Compiler Key and add to qualifier
                qualifier_items.append(find_key_by_values(items, compiler['ID'], compiler['Name'], compiler['Description']))

            qualifier = []
            for qualifier_item in qualifier_items:
                qualifier.extend([{"property": {"id": "P7"},"value": {"type": "value","content": qualifier_item}}])

            payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', hardware_item, 'wikibase-item', qualifier)
            
    # Add instruments the workflow uses
    for value in data.get('instrument').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        instrument_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier = []
        if value.get('Version'):
            qualifier.extend([{"property": {"id": "P568"},"value": {"type": "value","content": value['Version']}}])

        if value.get('SerialNumber'):
            qualifier.extend([{"property": {"id": "P587"},"value": {"type": "value","content": value['SerialNumber']}}])

        qualifier_locations = []
        for location in value.get('location', {}).values():
            # Use new ID if present
            location['ID'] = old_new.get((location['ID'], location['Name'], location['Description']), [''])[0] or location['ID']
            # Get Location Key and ad to Qualifier
            qualifier_locations.append(find_key_by_values(items, location['ID'], location['Name'], location['Description']))

        for qualifier_location in qualifier_locations:
            qualifier.extend([{"property": {"id": "P377"},"value": {"type": "value","content": qualifier_location}}])

        qualifier_softwares = []
        for software in value.get('software', {}).values():
            # Use new ID if present
            software['ID'] = old_new.get((software['ID'], software['Name'], software['Description']), [''])[0] or software['ID']
            # Get Software Key and ad to Qualifier
            qualifier_softwares.append(find_key_by_values(items, software['ID'], software['Name'], software['Description']))

        for qualifier_software in qualifier_softwares:
            qualifier.extend([{"property": {"id": "P7"},"value": {"type": "value","content": qualifier_software}}])

        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', instrument_item, 'wikibase-item', qualifier)
        
    # Add data sets the workflow uses
    for value in data.get('dataset').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        dataset_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', dataset_item)
        
    # Add Process Steps the workflow uses
    for value in data.get('processstep').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        processstep_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier = []
        for parameter in value.get('parameter').values():
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": parameter}}])

        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P7', processstep_item, 'wikibase-item', qualifier)
        
    # Add Publication about the Workflow
    for value in data.get('publication').values():
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        publication_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        payload, rel_idx = add_static_or_non_item_relation(payload, item, rel_idx, 'P18', publication_item)
        
    return payload


    
    
    
    
def items_uri():
    return 'https://staging.mardi4nfdi.org/w/rest.php/wikibase/v1/entities/items'

def items_payload(name, description):
    if description and description != 'No Description Provided!':
        return {"item": {"labels": {"en": name}, "descriptions": {"en": description}}} 
    else:
        return {"item": {"labels": {"en": name}}}

def statements_uri(item):
    return f'https://staging.mardi4nfdi.org/w/rest.php/wikibase/v1/entities/items/{item}/statements'

def statements_payload(id, content, data_type = "wikibase-item", qualifiers = []):
    return {"statement": {"property": {"id": id, "data_type": data_type}, "value": {"type": "value", "content": content}, "qualifiers": qualifiers}}

def unique_items(data, title):
    # Set up Item Dict and track seen Items
    items = {}
    seen_items = set() 
    # Add Workflow Item
    triple = ('not found', title, data.get('general', {}).get('objective', ''))
    items[f'Item{str(0).zfill(10)}'] = {'ID': 'not found', 'Name': title, 'Description': data.get('general', {}).get('objective', '')}
    seen_items.add(triple)
    # Add Workflow Component Items
    def search(subdict):
        if isinstance(subdict, dict) and 'ID' in subdict:
            triple = (subdict.get('ID', ''), subdict.get('Name', ''), subdict.get('Description', ''))
            if triple not in seen_items:
                item_key = f'Item{str(len(items)).zfill(10)}'  # Create unique key
                items[item_key] = {'ID': triple[0], 'Name': triple[1], 'Description': triple[2]}
                seen_items.add(triple)
        if isinstance(subdict, dict):
            for value in subdict.values():
                if isinstance(value, dict):
                    search(value)
    search(data)
    return items

def find_key_by_values(extracted_dict, id_value, name_value, description_value):
    for key, values in extracted_dict.items():
        if (values['ID'] == id_value and 
            values['Name'] == name_value and 
            values['Description'] == description_value):
            return key
    return None

def add_item_relation(payload, values, lookup, items, item, idx, property, qualifier = [], datatype = 'wikibase-item'):
    for value in values:
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = lookup.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Entry Key
        entry = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        # Add to Payload
        payload.update({f"RELATION{idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload(property, entry, datatype, qualifier)}}) 
        idx += 1
    return payload, idx

def add_static_or_non_item_relation(payload, item, idx, property, content, datatype = 'wikibase-item', qualifier = []):
    payload.update({f"RELATION{idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload(property, content, datatype, qualifier)}}) 
    idx += 1
    return payload, idx

