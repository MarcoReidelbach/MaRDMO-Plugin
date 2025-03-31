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
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(key), 'payload': statements_payload("P2", id, "external-id")}})
                    rel_idx += 1
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
                        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(key), 'payload': statements_payload('P915', value['ISSN'], 'external-id')}})
                        rel_idx += 1
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
                            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(key), 'payload': statements_payload('P33', value['orcid'], 'external-id')}}) 
                            rel_idx += 1
                        if value.get('zbmath'):
                            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(key), 'payload': statements_payload('P369', value['zbmath'], 'external-id')}}) 
                            rel_idx += 1

    # Add additional Algorithms / Methods Information
    for value in data.get('method').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        if 'mathalgodb' in value['ID']:
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q4629')}}) 
            rel_idx += 1
        else:
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q2822')}}) 
            rel_idx += 1

    # Add additional Software Information
    for value in data.get('software').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q420')}})
        rel_idx += 1
        
        # Add References of the Software
        for reference in value.get('Reference', {}).values():
            if reference[0] == options['DOI']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P27', reference[1], 'external-id')}}) 
                rel_idx += 1
            elif reference[0] == options['SWMATH']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P31', reference[1], 'external-id')}}) 
                rel_idx += 1
            elif reference[0] == options['URL']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P107', reference[1], 'external-id')}}) 
                rel_idx += 1
        
        # Add Programming Languages
        for entry in value.get('programminglanguage', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P30', entry_item)}}) 
            rel_idx += 1
        
        # Add Dependencies
        for entry in value.get('dependency', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P474', entry_item)}}) 
            rel_idx += 1
        
        # Add Source Code Repository
        if value.get('Published'):
            if value['Published'][0] == options['YesText']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P69', value['Published'][1], 'url')}}) 
                rel_idx += 1
        
        # Add Documentation / Manual
        if value.get('Documented'):
            if value['Documented'][0] == options['YesText']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P56', value['Documented'][1], 'url')}}) 
                rel_idx += 1

    # Add additional Hardware Information
    for value in data.get('hardware').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q387')}}) 
        rel_idx += 1
        
        # Add CPU
        for entry in value.get('cpu', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P585', entry_item)}}) 
            rel_idx += 1
        
        # Add Number of Nodes (Computing Nodes)
        if value.get('Nodes'):
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P124', 'Q13129', 'wikibase-item', [{"property":{"id":"P302"},"value":{"type":"value","content":{"amount":f"+{value['Nodes']}","unit":"1"}}}])}}) 
            rel_idx += 1
        
        # Add Number of Cores (Processor Cores)
        if value.get('Cores'):
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P588', {"amount":f"+{value['Cores']}","unit":"1"}, 'quantity')}})
            rel_idx += 1

    # Add additional Instrument Information
    for value in data.get('instrument').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q4682')}}) 
        rel_idx += 1

    # Add additional Data Set Information
    for value in data.get('dataset').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q381')}}) 
        rel_idx += 1

        # Size of the data set
        if value.get('Size'):
            if value['Size'][0] == options['kilobyte']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13145"}, 'quantity')}}) 
                rel_idx += 1
            elif value['Size'][0] == options['megabyte']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13146"}, 'quantity')}}) 
                rel_idx += 1
            elif value['Size'][0] == options['gigabyte']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13147"}, 'quantity')}}) 
                rel_idx += 1
            elif value['Size'][0] == options['terabyte']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P790', {"amount":f"+{value['Size'][1]}","unit":"https://staging.mardi4nfdi.org/entity/Q13148"}, 'quantity')}}) 
                rel_idx += 1
            elif value['Size'][0] == options['items']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P328', {"amount":f"+{value['Size'][1]}","unit":"1"}, 'quantity')}}) 
                rel_idx += 1
        
        # Data Type of the data set
        for entry in value.get('datatype', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q1917"}}]
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', entry_item, 'wikibase-item', qualifier)}}) 
            rel_idx += 1
        
        # Representation Format of the data set
        for entry in value.get('representationformat', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q13149"}}]
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', entry_item, 'wikibase-item', qualifier)}}) 
            rel_idx += 1
        
        # File Format of the Data Set
        if value.get('FileFormat'):
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P792', value['FileFormat'], 'string')}}) 
            rel_idx += 1
        
        # Data Set binary or text
        if value.get('BinaryText'):
            if value['BinaryText'] == options['binary']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q3742')}}) 
                rel_idx += 1
            elif value['BinaryText'] == options['text']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13150')}}) 
                rel_idx += 1
        
        # Data Set Proprietary
        if value.get('Proprietary'):
            if value['Proprietary'] == options['Yes']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q3747')}}) 
                rel_idx += 1
            elif value['Proprietary'] == options['No']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q3745')}}) 
                rel_idx += 1
        
        # Data Set To Publish
        if value.get('ToPublish'):
            if value['ToPublish'].get(0, ['',''])[0] == options['Yes']:
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P794', 'Q3743')}}) 
                rel_idx += 1
                if value['ToPublish'].get(1, ['',''])[0] == options['DOI']:
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P27', value['ToPublish'][1][1])}}) 
                    rel_idx += 1
                if value['ToPublish'].get(2, ['',''])[0] == options['URL']:
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P107', value['ToPublish'][2][1])}}) 
                    rel_idx += 1
        
        # Data Set To Archive
        if value.get('ToArchive'):
            if value['ToArchive'][0] == options['YesText']:
                qualifier = []
                if value['ToArchive'][1]:
                    qualifier = [{"property":{"id":"P791", 'data_type': 'time'},"value":{"type":"value","content":{"time":f"+{value['ToArchive'][1]}-00-00T00:00:00Z","precision":9,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}}}]
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P794', 'Q3748', 'wikibase-item', qualifier)}}) 
                rel_idx += 1

    # Add additional Process Step Information
    for value in data.get('processstep').values():
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = old_new.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key and add to Payload
        item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        # Add the class of the Process Step
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13152')}})
        rel_idx += 1
        
        # Add Input Data Sets
        for entry in value.get('input', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P1093', entry_item)}}) 
            rel_idx += 1
        
        # Add Output Data Sets
        for entry in value.get('output', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P1094', entry_item)}}) 
            rel_idx += 1
        
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
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', entry_item, 'wikibase-item', qualifier)}}) 
            rel_idx += 1
        
        # Add Software Environment
        for entry in value.get('environmentSoftware', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q420"}}]
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P402', entry_item, 'wikibase-item', qualifier)}}) 
            rel_idx += 1
        
        # Add Instrument Environment
        for entry in value.get('environmentInstrument', {}).values():
            # Continue if no ID exists
            if not entry.get('ID'):
                continue
            # Use new ID if present
            entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
            # Get Item Key and add to Payload
            entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
            qualifier = [{"property": {"id": "P293"},"value": {"type": "value","content": "Q4682"}}]
            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P402', entry_item, 'wikibase-item', qualifier)}}) 
            rel_idx += 1
        
        # Add Disciplines (math and non-math)
        for discipline in value.get('discipline', {}).values():
            # Check if new ID exists
            if 'msc:' in discipline.get('ID'):
                _, id = discipline['ID'].split(':')
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P349', id, 'external-id')}}) 
                rel_idx += 1
            else:
                # Check if new ID exists
                if (discipline.get('ID'), discipline.get('Name'), discipline.get('Description'))  in old_new.keys():
                    discipline['ID'] = old_new[(discipline['ID'], discipline['Name'], discipline['Description'])][0]
                # Get Item Key
                discipline_item = find_key_by_values(items, discipline['ID'], discipline['Name'], discipline['Description'])
                payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P19', discipline_item)}}) 
                rel_idx += 1

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
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q259' if value['entrytype'] == 'scholarly article' else 'Q428')}}) 
                    rel_idx += 1
                # Add the Title of the Publication
                if value.get('title'):
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P15', {"text": value['title'], "language": "en"}, 'monolingualtext')}}) 
                    rel_idx += 1
                # Add the Volume of the Publication
                if value.get('volume'):
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P24', value['volume'], 'string')}}) 
                    rel_idx += 1
                # Add the Issue of the Publication
                if value.get('issue'):
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P25', value['issue'], 'string')}}) 
                    rel_idx += 1
                # Add the Page(s) of the Publication
                if value.get('page'):
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P26', value['page'], 'string')}}) 
                    rel_idx += 1
                # Add the Date of the Publication
                if value.get('date'):
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P22', {"time":f"+{value['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}, 'time')}}) 
                    rel_idx += 1
                # Add the DOI of the Publication
                if value.get('reference', {}).get(0):
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P27', value['reference'][0][1], 'external-id')}}) 
                    rel_idx += 1
                # Add the Language of the Publication
                for entry in value.get('language', {}).values():
                    # Continue if no ID exists
                    if not entry.get('ID'):
                        continue
                    # Use new ID if present
                    entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
                    # Get Item Key and add to Payload
                    entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P6', entry_item)}})
                    rel_idx += 1
                # Add the Journal of the Publication
                for entry in value.get('journal', {}).values():
                    # Continue if no ID exists
                    if not entry.get('ID'):
                        continue
                    # Use new ID if present
                    entry['ID'] = old_new.get((entry['ID'], entry['Name'], entry['Description']), [''])[0] or entry['ID']
                    # Get Item Key and add to Payload
                    entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
                    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P23', entry_item)}}) 
                    rel_idx += 1
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
                        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P20', entry_item)}}) 
                        rel_idx += 1
                    else:
                        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P21', entry['Name'], 'string')}}) 
                        rel_idx += 1

    # Add Interdisciplinary Workflow Information
    if ('not found', title, data.get('general', {}).get('objective')) in old_new.keys():
        workflow_id = old_new[('not found', title, data.get('general', {}).get('objective'))][0]
    else:
        workflow_id = 'not found'

    item = find_key_by_values(items, workflow_id, title, data.get('general', {}).get('objective'))
    
    # Add instance of research workflow
    payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q18')}}) 
    rel_idx += 1

    # Add description to the Workflow
    if data.get('general', {}).get('procedure'):
       payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P896', data['general']['procedure'])}})
       rel_idx += 1 

    # Add Reproducibility Aspects
    if data.get('reproducibility', {}).get('mathematical') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('mathematicalcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['mathematicalcondition']}}])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13160', 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    if data.get('reproducibility', {}).get('runtime') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('runtimecondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['runtimecondition']}}])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13162', 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    if data.get('reproducibility', {}).get('result') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('resultcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['resultcondition']}}])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13163', 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    if data.get('reproducibility', {}).get('originalplatform') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('originalplatformcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['originalplatformcondition']}}])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13164', 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    if data.get('reproducibility', {}).get('otherplatform') == options['Yes']:
        qualifier = []
        if data['reproducibility'].get('otherplatformcondition'):
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": data['reproducibility']['otherplatformcondition']}}])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13165', 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    if data.get('reproducibility', {}).get('transferability'):
        qualifier = []
        for value in data['reproducibility']['transferability'].values():
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": value}}])
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P3', 'Q13166', 'wikibase-item', qualifier)}}) 
        rel_idx += 1
    
    # Add methods the workflow uses
    for _, value in data.get('method').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        method_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier_strings = []
        for parameter in value.get('Parameter').values():
            qualifier_strings.append(parameter)
        
        qualifier_items = []
        for software in value.get('software', {}).values():
            if (software.get('ID'), software.get('Name'), software.get('Description')) in old_new.keys():
                    software['ID'] = old_new[(software['ID'], software['Name'], software['Description'])][0]
            qualifier_items.append(find_key_by_values(items, software['ID'], software['Name'], software['Description']))
        
        for instrument in value.get('instrument', {}).values():
            if (instrument.get('ID'), instrument.get('Name'), instrument.get('Description')) in old_new.keys():
                    instrument['ID'] = old_new[(instrument['ID'], instrument['Name'], instrument['Description'])][0]
            qualifier_items.append(find_key_by_values(items, instrument['ID'], instrument['Name'], instrument['Description']))
        
        qualifier = []
        for qualifier_item in qualifier_items:
            qualifier.extend([{"property": {"id": "P1089"},"value": {"type": "value","content": qualifier_item}}])

        for qualifier_string in qualifier_strings:
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": qualifier_string}}])

        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', method_item, 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    # Add software the workflow uses
    for _, value in data.get('software').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        software_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier = []
        for hardware in data.get('hardware').values():
            for software in hardware.get('software').values():
                if software.get('ID') == value['ID'] and software.get('Name') == value['Name'] and software.get('Description') == value['Description']:
                    hardware_item = find_key_by_values(items, hardware['ID'], hardware['Name'], hardware['Description'])
                    qualifier.extend([{"property": {"id": "P402"},"value": {"type": "value","content": hardware_item}}])
        
        if value.get('Version'):
            qualifier = [{"property": {"id": "P472"},"value": {"type": "value","content": value['Version']}}]
            
        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', software_item, 'wikibase-item', qualifier)}}) 
        rel_idx += 1
        
    # Add hardware the workflow uses
    for _, value in data.get('hardware').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        if value.get('ID'):
            hardware_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

            qualifier_items = []
            for compiler in value.get('compiler', {}).values():
                if (compiler.get('ID'), compiler.get('Name'), compiler.get('Description')) in old_new.keys():
                        compiler['ID'] = old_new[(compiler['ID'], compiler['Name'], compiler['Description'])][0]
                qualifier_items.append(find_key_by_values(items, compiler['ID'], compiler['Name'], compiler['Description']))

            qualifier = []
            for qualifier_item in qualifier_items:
                qualifier.extend([{"property": {"id": "P7"},"value": {"type": "value","content": qualifier_item}}])

            payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', hardware_item, 'wikibase-item', qualifier)}}) 
            rel_idx += 1

    # Add instruments the workflow uses
    for _, value in data.get('instrument').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        instrument_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier = []
        if value.get('Version'):
            qualifier.extend([{"property": {"id": "P568"},"value": {"type": "value","content": value['Version']}}])

        if value.get('SerialNumber'):
            qualifier.extend([{"property": {"id": "P587"},"value": {"type": "value","content": value['SerialNumber']}}])

        qualifier_locations = []
        for location in value.get('location', {}).values():
            if (location.get('ID'), location.get('Name'), location.get('Description')) in old_new.keys():
                    location['ID'] = old_new[(location['ID'], location['Name'], location['Description'])][0]
            qualifier_locations.append(find_key_by_values(items, location['ID'], location['Name'], location['Description']))

        for qualifier_location in qualifier_locations:
            qualifier.extend([{"property": {"id": "P377"},"value": {"type": "value","content": qualifier_location}}])

        qualifier_softwares = []
        for software in value.get('software', {}).values():
            if (software.get('ID'), software.get('Name'), software.get('Description')) in old_new.keys():
                    software['ID'] = old_new[(software['ID'], software['Name'], software['Description'])][0]
            qualifier_softwares.append(find_key_by_values(items, software['ID'], software['Name'], software['Description']))

        for qualifier_software in qualifier_softwares:
            qualifier.extend([{"property": {"id": "P7"},"value": {"type": "value","content": qualifier_software}}])

        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', instrument_item, 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    # Add data sets the workflow uses
    for _, value in data.get('dataset').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        dataset_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', dataset_item)}})  
        rel_idx += 1

    # Add Process Steps the workflow uses
    for _, value in data.get('processstep').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        processstep_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        qualifier = []
        for parameter in value.get('parameter').values():
            qualifier.extend([{"property": {"id": "P1092"},"value": {"type": "value","content": parameter}}])

        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P7', processstep_item, 'wikibase-item', qualifier)}}) 
        rel_idx += 1

    # Add Publication about the Workflow
    for _, value in data.get('publication').items():
        if (value.get('ID'), value.get('Name'), value.get('Description'))  in old_new.keys():
            value['ID'] = old_new[(value['ID'], value['Name'], value['Description'])][0]
        publication_item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])

        payload.update({f"RELATION{rel_idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload('P18', publication_item)}}) 
        rel_idx += 1

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

def add_simple_relation(payload, entry, dict, items, item, idx, property, qualifier = []):
    # Check if new ID exists
    if (entry.get('ID'), entry.get('Name'), entry.get('Description'))  in dict.keys():
        entry['ID'] = dict[(entry['ID'], entry['Name'], entry['Description'])][0]
    # Get Item Key
    if entry.get('ID'):
        entry_item = find_key_by_values(items, entry['ID'], entry['Name'], entry['Description'])
        payload.update({f"RELATION{idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload(property, entry_item, 'wikibase-item', qualifier)}}) 
        idx += 1
    return payload, idx
