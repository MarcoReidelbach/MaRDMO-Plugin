'''Module containing Utility Functions for the Algorithm Documentation'''

import re

from .constants import class_prefix_map

from ..constants import BASE_URI
from ..helpers import value_editor
from ..getters import get_data, get_mathalgodb, get_options
from ..queries import query_sparql

def update_ids(project, ids, query, sparql_endpoint, source):
    """Update IDs of new MathAlgoDB Items and add them to the Questionnaire"""
    new_ids = {}

    for key, id_value in ids.items():
        # Ignore Items with MathAlgoDB ID
        if id_value.startswith(('mathmoddb:', 'bm:', 'pr:', 'so:', 'al:', 'pb')):
            continue

        # Get MathAlgoDB ID
        results = query_sparql(query.format(f'"{key}"'), sparql_endpoint)
        if not (results and results[0].get('ID', {}).get('value')):
            continue

        match = re.match(r"(\d+)(\D+)", id_value)
        if not match:
            continue

        set_index, set_name = match.groups()
        first_result = results[0]

        # Generate Entry
        value_editor(
            project=project,
            uri=f"{BASE_URI}domain/{set_name}/id",
            info = {
                'text': f"{key} ({first_result['quote']['value']}) [{source}]",
                'external_id': f"{source}:{first_result['ID']['value']}",
                'set_index': set_index
            }
        )

        if source == 'mathalgodb':
            class_value = first_result.get('class', {}).get('value')
            if not class_value:
                continue
            prefix = class_prefix_map.get(class_value)
            if prefix:
                new_ids[key] = f"{prefix}:{first_result['ID']['value']}"

    return new_ids

def dict_to_triples_mathalgodb(data):
    '''Turn Dictionary Entries into Subject-Predicate-Object Triples'''
    mathalgodb = get_mathalgodb()
    inverse_property_mapping = get_data('algorithm/data/inversePropertyMapping.json')
    options = get_options()

    relations = ['IntraClassRelation', 'P2A', 'P2B', 'P2S']
    relatants = ['IntraClassElement', 'ARelatant', 'BRelatant', 'SRelatant']

    triples = []
    ids = {}

    # Get ID Dict
    for idx, item in data.items():
        if item['ID'] and item['ID'].startswith('mathalgodb:'):
            _, mathalgodb_id = item['ID'].split(':')
            if 'algorithm' in idx:
                ids[item['Name']] = f"al:{mathalgodb_id}"
            if 'problem' in idx:
                ids[item['Name']] = f"pr:{mathalgodb_id}"
            if 'benchmark' in idx:
                ids[item['Name']] = f"bm:{mathalgodb_id}"
            if 'software' in idx:
                ids[item['Name']] = f"so:{mathalgodb_id}"
            if 'publication' in idx:
                ids[item['Name']] = f"pb:{mathalgodb_id}"
        else:
            ids[item['Name']] = idx

    # Go through all individuals
    for idx, item in data.items():

        # Get ID of Individual
        subject = ids[item['Name']]

        if not subject.startswith(("al:", "pr:", "so:", "pb:", "bm:", "mathalgodb:")):

            # Assign Individual Label
            triples.append((subject, "rdfs:label", f'"{item["Name"]}"'))

            # Assign Individual Description
            if item.get('Description'):
                if item['Description'] != 'No Description Provided!':
                    triples.append((subject, "rdfs:comment", f'"{item["Description"]}"'))

            # Assign Individual Class
            if 'algorithm' in idx:
                triples.append((subject, "a", 'mathalgodb:algorithm'))
            elif 'problem' in idx:
                triples.append((subject, "a", 'mathalgodb:problem'))
            elif 'software' in idx:
                triples.append((subject, "a", 'mathalgodb:software'))
            elif 'benchmark' in idx:
                triples.append((subject, "a", 'mathalgodb:benchmark'))
            elif 'publication' in idx:
                triples.append((subject, "a", 'mathalgodb:publication'))

            # Assign Individual References
            for reference in item.get('reference', {}).values():
                if reference[0] == options['DOI']:
                    doi_value = reference[1]
                    triples.append((subject, "dc:hasIdentifier", f'"doi:{doi_value}"'))
                if reference[0] == options['SWMATH']:
                    swmath_value = reference[1]
                    triples.append((subject, "dc:hasIdentifier", f'"swmath:{swmath_value}"'))
                if reference[0] == options['MORWIKI']:
                    morwiki_value = reference[1]
                    triples.append((subject, "dc:hasIdentifier", f'"morwiki:{morwiki_value}"'))
                if reference[0] == options['URL']:
                    url_value = reference[1]
                    triples.append((subject, "dc:hasIdentifier", f'"{url_value}"'))

        # Assign Individual Relations
        if 'algorithm' in idx:
            for relatant in ['PRelatant', 'SRelatant']:
                relatant_dict = item.get(relatant, {})
                for key in relatant_dict:
                    relation_uri = None
                    if relatant == 'PRelatant':
                        relation_uri = mathalgodb['solves']
                    elif relatant == 'SRelatant':
                        relation_uri = mathalgodb['implementedBy']
                    relatant_value = relatant_dict[key]
                    object_value = None
                    if relatant_value['ID'].startswith('mathalgodb:'):
                        _, mathalgodb_id = relatant_value['ID'].split(':')
                        if relatant == 'PRelatant':
                            object_value = f"pr:{mathalgodb_id}"
                        elif relation == 'SRelatant':
                            object_value = f"so:{mathalgodb_id}"
                    else:
                        referred_name = relatant_value['Name']
                        object_value = ids.get(referred_name)
                    triples.append(
                        (subject,
                         f"mathalgodb:{relation_uri.split('/')[-1]}",
                         object_value)
                    )
                    triples.append(
                        (object_value,
                         f"mathalgodb:{inverse_property_mapping[relation_uri].split('/')[-1]}",
                         subject)
                    )

        # Assign Individual Relations
        if 'problem' in idx:
            for relatant in ['BRelatant']:
                relatant_dict = item.get(relatant, {})
                for key in relatant_dict:
                    if relatant == 'BRelatant':
                        relation_uri = mathalgodb['instantiates']
                    relatant_value = relatant_dict[key]
                    if relatant_value['ID'].startswith('mathalgodb:'):
                        _, mathalgodb_id = relatant_value['ID'].split(':')
                        if relatant == 'BRelatant':
                            object_value = f"bm:{mathalgodb_id}"
                    else:
                        referred_name = relatant_value['Name']
                        object_value = ids.get(referred_name)
                    triples.append(
                        (subject,
                         f"mathalgodb:{relation_uri.split('/')[-1]}",
                         object_value)
                    )
                    triples.append(
                        (object_value,
                         f"mathalgodb:{inverse_property_mapping[relation_uri].split('/')[-1]}",
                         subject)
                    )

        # Assign Individual Relations
        if 'software' in idx:
            for relatant in ['BRelatant']:
                relatant_dict = item.get(relatant, {})
                for key in relatant_dict:
                    if relatant == 'BRelatant':
                        relation_uri = mathalgodb['tests']
                    relatant_value = relatant_dict[key]
                    if relatant_value['ID'].startswith('mathalgodb:'):
                        _, mathalgodb_id = relatant_value['ID'].split(':')
                        if relatant == 'BRelatant':
                            object_value = f"bm:{mathalgodb_id}"
                    else:
                        referred_name = relatant_value['Name']
                        object_value = ids.get(referred_name)
                    triples.append(
                        (subject,
                         f"mathalgodb:{relation_uri.split('/')[-1]}",
                         object_value)
                    )
                    triples.append(
                        (object_value,
                         f"mathalgodb:{inverse_property_mapping[relation_uri].split('/')[-1]}",
                         subject)
                    )

        # Assign Further Relations
        for relation, relatant in zip(relations,relatants):
            relation_dict = item.get(relation, {})
            relatant_dict = item.get(relatant, {})
            for key in relation_dict:
                if relatant_dict.get(key):
                    relation_uri = relation_dict[key]
                    relatant_values = relatant_dict[key]
                    for relatant_value in relatant_values.values():
                        if relatant_value['ID'].startswith('mathalgodb:'):
                            _, mathalgodb_id = relatant_value['ID'].split(':')
                            if relation == 'IntraClassRelation':
                                if 'algorithm' in idx:
                                    object_value = f"al:{mathalgodb_id}"
                                if 'problem' in idx:
                                    object_value = f"pr:{mathalgodb_id}"
                                if 'benchmark' in idx:
                                    object_value = f"bm:{mathalgodb_id}"
                                if 'software' in idx:
                                    object_value = f"so:{mathalgodb_id}"
                                if 'publication' in idx:
                                    object_value = f"pb:{mathalgodb_id}"
                            elif relation == 'P2A':
                                object_value = f"al:{mathalgodb_id}"
                            elif relation == 'P2B':
                                object_value = f"bm:{mathalgodb_id}"
                            elif relation == 'P2S':
                                object_value = f"so:{mathalgodb_id}"
                        else:
                            referred_name = relatant_value['Name']
                            object_value = ids.get(referred_name)
                        triples.append(
                            (subject,
                             f"mathalgodb:{relation_uri.split('/')[-1]}",
                             object_value)
                        )
                        triples.append(
                            (object_value,
                             f"mathalgodb:{inverse_property_mapping[relation_uri].split('/')[-1]}",
                             subject)
                        )

    return triples, ids

def generate_sparql_insert_with_new_ids_mathalgodb(triples):
    '''Generate SPARQL Insert Query'''
    # Step 1: Identify new items that need mardmo IDs
    new_items = {}
    counter = 0
    for triple in triples:
        subject = triple[0]
        if not subject.startswith(("al:", "pr:", "so:", "pb:", "bm:", "mathalgodb:")):
            # Assign temporary placeholders for new IDs
            new_items[subject] = f"newItem{counter}"
            counter += 1

    # Step 2: Generate SPARQL query with BIND for new mardmo IDs
    insert_query = """
    PREFIX mathalgodb: <https://mardi4nfdi.de/mathalgodb/0.1#>
    PREFIX bm: <https://mardi4nfdi.de/mathalgodb/0.1/benchmark#>
    PREFIX al: <https://mardi4nfdi.de/mathalgodb/0.1/algorithm#>
    PREFIX so: <https://mardi4nfdi.de/mathalgodb/0.1/software#>
    PREFIX pr: <https://mardi4nfdi.de/mathalgodb/0.1/problem#>
    PREFIX pb: <https://mardi4nfdi.de/mathalgodb/0.1/publication#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dc: <http://purl.org/spar/datacite/>

    INSERT{
    """
    # Construct the insert part
    for triple in triples:
        subject = triple[0]
        predicate = triple[1]
        obj = triple[2]

        # Replace new subjects with placeholders
        if subject in new_items:
            subject = f"?{new_items[subject]}"
        else:
            subject = f"{subject}"

        # Format object based on whether it's a literal or a URI
        if re.match(r'^https?://', obj):
            obj_formatted = f"<{obj}>"
        else:
            if obj.startswith(("al:", "pr:", "so:", "pb:", "bm:", "mathalgodb:", '"', ':', '<')):
                obj_formatted = f'{obj}'
            else:
                obj_formatted = f"?{new_items[obj]}"

        # Construct the triple in the query
        insert_query += f"  {subject} {predicate} {obj_formatted} .\n"

    insert_query += "}\nWHERE {\n"

    # Step 3: Add logic to get the next free mardmo ID
    insert_query += """
    {
      SELECT (MAX(?num) AS ?maxID) WHERE {
        ?id a ?type .
        FILTER (
          STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathalgodb/0.1/benchmark#mardmo") ||
          STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathalgodb/0.1/problem#mardmo") ||
          STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathalgodb/0.1/software#mardmo") ||
          STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathalgodb/0.1/algorithm#mardmo") ||
          STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathalgodb/0.1/publication#mardmo")
        )
        BIND (xsd:integer(REPLACE(STR(?id), ".*#mardmo", "")) AS ?num)
      }
    }
    BIND (IF(BOUND(?maxID), ?maxID + 1, 0) AS ?nextID)
    """
    id_counter = 0
    for new_item in new_items:

        if 'algorithm' in new_item:
            insert_query += (
                "BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/algorithm"
                f"#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
            )
        elif 'benchmark' in new_item:
            insert_query += (
                "BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/benchmark"
                f"#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
            )
        elif 'software' in new_item:
            insert_query += (
                "BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/software"
                f"#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
            )
        elif 'problem' in new_item:
            insert_query += (
                "BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/problem"
                f"#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
            )
        elif 'publication' in new_item:
            insert_query += (
                "BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/publication"
                f"#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
            )

        id_counter += 1

    insert_query += "}"

    return insert_query
