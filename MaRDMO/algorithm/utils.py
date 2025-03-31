import re

from rdmo.domain.models import Attribute

from ..config import BASE_URI
from ..utils import extract_parts, get_data


def get_answer_algorithm(project, val, uri, key1 = None, key2 = None, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
    '''Function to get user answers into dictionary.'''
    val.setdefault(key1, {})
    
    try:
        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f"{BASE_URI}{uri}"))
    except:
        values = []

    if not (key1 or key2):
        values =[]

    for value in values:
        if value.option:
            if set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.option_uri})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
        elif value.text:
            if not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.text})
            elif not set_prefix and set_index and not collection_index and external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.external_id})
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.text})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})    
            elif set_prefix and not set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:f"{value.external_id} <|> {label}"})
            elif set_prefix and set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:f"{value.external_id} <|> {label}"})    
    return val

def dict_to_triples_mathalgodb(data):

    inversePropertyMapping = get_data('algorithm/data/inversePropertyMapping.json')
    options = get_data('data/options.json')

    relations = ['IntraClassRelation', 'A2P', 'A2S', 'P2B', 'S2B', 'P2A', 'P2B', 'P2S']
    relatants = ['IntraClassElement', 'PRelatant', 'SRelatant', 'BRelatant', 'BRelatant', 'ARelatant', 'BRelatant', 'SRelatant']
    
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
        
        # Assign Individual Properties
        for relation, relatant in zip(relations,relatants):
            relation_dict = item.get(relation, {})
            relatant_dict = item.get(relatant, {})
            for key in relation_dict:
                if relatant_dict.get(key):
                    relation_uri = relation_dict[key]
                    relatant_value = relatant_dict[key].split(' <|> ')
                    if relatant_value[0].startswith('mathalgodb:'):
                        _, mathalgodb_id = relatant_value[0].split(':')
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
                        elif relation == 'A2P':
                            object_value = f"pr:{mathalgodb_id}"
                        elif relation == 'A2S':
                            object_value = f"so:{mathalgodb_id}"
                        elif relation == 'P2B':
                            object_value = f"bm:{mathalgodb_id}"
                        elif relation == 'S2B':
                            object_value = f"bm:{mathalgodb_id}"
                        elif relation == 'P2A':
                            object_value = f"al:{mathalgodb_id}"
                        elif relation == 'P2B':
                            object_value = f"bm:{mathalgodb_id}"
                        elif relation == 'P2S':
                            object_value = f"so:{mathalgodb_id}"
                    else:
                        referred_name = relatant_value[1]
                        object_value = ids.get(referred_name)
                    triples.append((subject, f"mathalgodb:{relation_uri.split('/')[-1]}", object_value))
                    triples.append((object_value, f"mathalgodb:{inversePropertyMapping[relation_uri].split('/')[-1]}", subject))
    
    return triples, ids

def generate_sparql_insert_with_new_ids_mathalgodb(triples):
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
            if obj.startswith(("al:", "pr:", "so:", "pb:", "bm:", "mathalgodb:")) or obj.startswith('"') or obj.startswith(':') or obj.startswith('<'):
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
            insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/algorithm#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        elif 'benchmark' in new_item:
            insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/benchmark#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        elif 'software' in new_item:
            insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/software#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        elif 'problem' in new_item:
            insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/problem#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        elif 'publication' in new_item:
            insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathalgodb/0.1/publication#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        
        id_counter += 1

    insert_query += "}"

    return insert_query
