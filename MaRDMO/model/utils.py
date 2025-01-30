import re

from rdmo.options.models import Option
from rdmo.domain.models import Attribute

from ..config import BASE_URI
from ..utils import extract_parts, get_data, value_editor

from .sparql import queryHandler

def add_basics(instance, url_name, url_description):
    label, description, _ = extract_parts(instance.text)
    value_editor(instance.project, url_name, label, None, None, None, 0, instance.set_index)
    value_editor(instance.project, url_description, description, None, None, None, 0, instance.set_index)
    return

def add_entity(instance, results, url_set, url_id, prop, prefix):
    set_ids = get_id(instance, url_set, ['set_index'])
    value_ids = get_id(instance, url_id, ['external_id'])
    # Add Research Field entry to questionnaire
    idx = max(set_ids, default = -1) + 1
    if results[0].get(prop, {}).get('value'):
        IDs = results[0][prop]['value'].split(' / ')
        Labels = results[0][f'{prop}Label']['value'].split(' / ')
        Descriptions = results[0][f'{prop}Description']['value'].split(' / ')
        for ID, Label, Description in zip(IDs, Labels, Descriptions):
            if f"mathmoddb:{ID}" not in value_ids:
                # Set up Page
                value_editor(instance.project, url_set, f"{prefix}{idx}", None, None, None, idx)
                # Add ID Values
                value_editor(instance.project, url_id, f'{Label} ({Description}) [mathmoddb]', f"mathmoddb:{ID}", None, None, idx)
                idx += 1
                value_ids.append(f"mathmoddb:{ID}")

def add_properties(instance, results, mathmoddb, url_properties):
    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
        if results[0].get(prop, {}).get('value') == 'true':
            value_editor(instance.project, url_properties, None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
    return

def add_relations(instance, results, mathmoddb, url_relation, url_relatant, props, relation = True, appendix = '', set_prefix = None, collection_index = False):
    if set_prefix == None:
        set_prefix = instance.set_index
    idx = 0
    for prop in props:
        if results[0].get(f'{prop}{appendix}', {}).get('value'):
            IDs = results[0][f'{prop}{appendix}']['value'].split(' / ')
            Labels = results[0][f'{prop}{appendix}Label']['value'].split(' / ')
            Descriptions = results[0][f'{prop}{appendix}Description']['value'].split(' / ')
            for ID, Label, Description in zip(IDs, Labels, Descriptions):
                if relation:
                    if collection_index:
                        value_editor(instance.project, url_relation, None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, set_prefix)
                    else:
                        value_editor(instance.project, url_relation, None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, set_prefix)
                if collection_index:
                    value_editor(instance.project, url_relatant, f"{Label} ({Description}) [mathmoddb]", f'mathmoddb:{ID}', None, idx, 0, set_prefix)
                else:
                    value_editor(instance.project, url_relatant, f"{Label} ({Description}) [mathmoddb]", f'mathmoddb:{ID}', None, None, idx, set_prefix)
                idx += 1
    return

def get_id(instance, uri, keys):
    values = instance.project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
    ids = []
    if len(keys) == 1:
        for value in values:
            ids.append(getattr(value, keys[0]))
    else:
        for value in values:
            id = []
            for key in keys:
                id.append(getattr(value, key))
            ids.append(id)
    return ids 

def get_answer_model(project, val, uri, key1, key2, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
    '''Function to get user answers into dictionary.'''
    val.setdefault(key1, {})
    
    try:
        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f"{BASE_URI}{uri}"))
    except:
        values = []

    for value in values:
        if value.option:
            if not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.option_uri})
            elif not set_prefix and set_index and not collection_index and not external_id and option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:[value.option_uri, value.text]})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(int(value.set_prefix), {}).update({key2:value.option_uri})
            elif set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.option_uri})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key2 == 'reference':
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.option_uri})      
        elif value.text:
            if not set_prefix and not set_index and not collection_index and not external_id and not option_text:
                val[key1].update({key2:value.text})
            elif not set_prefix and not set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(key2, {}).update({value.collection_index:value.text})
            elif not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.text})
            elif not set_prefix and set_index and not collection_index and external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.external_id})
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.text})
            elif set_prefix and not set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.external_id})    
            elif set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({key3:value.text})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.text})
            elif set_prefix and set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({key3:f"{value.external_id} <|> {label}"})
                else: 
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:f"{value.external_id} <|> {label}"})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})    
            elif set_prefix and not set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:f"{value.external_id} <|> {label}"})
                
    return val

def dict_to_triples_mathmoddb(data):

    inversePropertyMapping = get_data('model/data/inversePropertyMapping.json')
    options = get_data('data/options.json')

    relations = ['IntraClassRelation','RP2RF','MM2RP','MF2MM','MF2MF','Q2Q','Q2QK','QK2Q','QK2QK','T2MF','T2Q','T2MM','P2E']
    relatants = ['IntraClassElement','RFRelatant','RPRelatant','MMRelatant','MFRelatant','QRelatant','QKRelatant','QRelatant','QKRelatant','MFRelatant','QRelatant','MMRelatant','EntityRelatant']
    
    triples = []
    ids = {} 
    
    # Get ID Dict
    for idx, item in data.items():
        if item['ID'] and item['ID'].startswith('mathmoddb:'):
            ids[item['Name']] = item['ID']
        else:
            ids[item['Name']] = idx
    
    # Go through all individuals
    for idx, item in data.items():

        # Get ID of Individual
        subject = ids[item['Name']]
        
        if not subject.startswith('mathmoddb:'):
        
            # Assign Individual Label 
            triples.append((subject, "rdfs:label", f'"{item["Name"]}"@en'))
        
            # Assign Individual Description
            if item.get('Description'):
                triples.append((subject, "rdfs:comment", f'"{item["Description"]}"@en'))
        
            # Assign Individual Class
            if 'field' in idx:
                triples.append((subject, "a", 'mathmoddb:ResearchField'))
            elif 'problem' in idx:
                triples.append((subject, "a", 'mathmoddb:ResearchProblem'))
            elif 'model' in idx:
                triples.append((subject, "a", 'mathmoddb:MathematicalModel'))
            elif 'quantity' in idx:
                if item['QorQK'] == 'https://rdmo.mardi4nfdi.de/terms/options/MathModDB/Quantity':
                    triples.append((subject, "a", 'mathmoddb:Quantity'))
                else:
                    triples.append((subject, "a", 'mathmoddb:QuantityKind'))
            elif 'formulation' in idx:
                triples.append((subject, "a", 'mathmoddb:MathematicalFormulation'))
            elif 'task' in idx:
                if item.get('TaskClass') == 'https://rdmo.mardi4nfdi.de/terms/options/MathModDB/ComputationalTask':
                    triples.append((subject, "a", 'mathmoddb:ComputationalTask'))
            elif 'publication' in idx:
                triples.append((subject, "a", 'mathmoddb:Publication'))
        
            # Assign Individual MaRDI/Wikidata ID
            if item.get('ID'):
                if item['ID'].startswith('wikidata:'):
                    q_number = item['ID'].split(':')[-1]
                    triples.append((subject, "mathmoddb:wikidataID", f'"{q_number}"'))
                elif item['ID'].startswith('mardi:'):
                    q_number = item['ID'].split(':')[-1]
                    triples.append((subject, "mathmoddb:mardiID", f'"{q_number}"'))

            # Assign Individual DOI/QUDT ID
            if item.get('reference'):
                if item['reference'].get(0):
                    if item['reference'][0][0] == options['DOI']:
                        doi_value = item['reference'][0][1]
                        triples.append((subject, "mathmoddb:doiID", f'<https://doi.org/{doi_value}>'))
                    if item['reference'][0][0] == options['QUDT']:
                        qudt_value = item['reference'][0][1]
                        triples.append((subject, "mathmoddb:qudtID", f'"{qudt_value}"'))
        
            # Assign Quantity definey by Individual
            if item.get('DefinedQuantity'):
                defined_quantity = item['DefinedQuantity'].split(' <|> ')
                if defined_quantity[0].startswith('mathmoddb:'):
                    object_value = defined_quantity[0]
                else:
                    #referred_name = defined_quantity[1]
                    object_value = ids.get(referred_name)
                triples.append((subject, 'mathmoddb:defines', object_value))
                triples.append((object_value, 'mathmoddb:definedBy', subject))
        
            # Assign Individual Formula
            if item.get('Formula'):
                formulas = item['Formula'].values()
                for formula in formulas:
                    formula = formula.replace('\\', '\\\\')
                    triples.append((subject, 'mathmoddb:definingFormulation', f'"{formula[1:-1]}"^^<https://mardi4nfdi.de/mathmoddb#LaTeX>'))
                if item.get('Element'):
                    elements = item['Element'].values()
                    for element in elements:
                        symbol = element['Symbol'].replace('\\', '\\\\')
                        quantity = element['quantity'].split(' <|> ')
                        if len(quantity) == 1:
                            referred_name = quantity[0]
                            object_value = ids.get(referred_name)
                        else:
                            if quantity[0].startswith('mathmoddb:'):
                                referred_name = quantity[1]
                                object_value = quantity[0]
                            else:
                                referred_name = quantity[1]
                                object_value = ids.get(referred_name)
                        if object_value:
                            triples.append((subject, 'mathmoddb:inDefiningFormulation', f'"{symbol[1:-1]}, {referred_name}"^^<https://mardi4nfdi.de/mathmoddb#LaTeX>'))
                            triples.append((subject, 'mathmoddb:containsQuantity', object_value))
                            triples.append((object_value, 'mathmoddb:containedInFormulation', subject))
        
            # Assign Individual Properties
            if item.get('Properties'):
                prefix = 'https://rdmo.mardi4nfdi.de/terms/options/MathModDB/'
                values = item['Properties'].values()
                if prefix + 'isLinear' in values:
                    triples.append((subject, "mathmoddb:isLinear", '"true"^^xsd:boolean'))
                elif prefix + 'isNotLinear' in values:
                    triples.append((subject, "mathmoddb:isLinear", '"false"^^xsd:boolean'))
                if prefix + 'isConvex' in values:
                    triples.append((subject, "mathmoddb:isConvex", '"true"^^xsd:boolean'))
                elif prefix + 'isNotConvex' in values:
                    triples.append((subject, "mathmoddb:isConvex", '"false"^^xsd:boolean'))
                if prefix + 'isDeterministic' in values:
                    triples.append((subject, "mathmoddb:isDeterministic", '"true"^^xsd:boolean'))
                elif prefix + 'isStochastic' in values:
                    triples.append((subject, "mathmoddb:isDeterministic", '"false"^^xsd:boolean'))
                if prefix + 'isDimensionless' in values:
                    triples.append((subject, "mathmoddb:isDimensionless", '"true"^^xsd:boolean'))
                elif prefix + 'isDimensional' in values:
                    triples.append((subject, "mathmoddb:isDimensionless", '"false"^^xsd:boolean'))
                if prefix + 'isDynamic' in values:
                    triples.append((subject, "mathmoddb:isDynamic", '"true"^^xsd:boolean'))
                elif prefix + 'isStatic' in values:
                    triples.append((subject, "mathmoddb:isDynamic", '"false"^^xsd:boolean'))
                if prefix + 'isSpaceContinuous' in values:
                    triples.append((subject, "mathmoddb:isSpaceContinuous", '"true"^^xsd:boolean'))
                elif prefix + 'isSpaceDiscrete' in values:
                    triples.append((subject, "mathmoddb:isSpaceContinuous", '"false"^^xsd:boolean'))
                if prefix + 'isTimeContinuous' in values:
                    triples.append((subject, "mathmoddb:isTimeContinuous", '"true"^^xsd:boolean'))
                elif prefix + 'isTimeDiscrete' in values:
                    triples.append((subject, "mathmoddb:isTimeContinuous", '"false"^^xsd:boolean'))	

        # Assign Individual Properties
        for relation, relatant in zip(relations,relatants):
            relation_dict = item.get(relation, {})
            relatant_dict = item.get(relatant, {})
            for key in relation_dict:
                if relatant_dict.get(key):
                    relation_uri = relation_dict[key]
                    relatant_value = relatant_dict[key].split(' <|> ')
                    if relatant_value[0].startswith('mathmoddb:'):
                        object_value = relatant_value[0]
                    else:
                        referred_name = relatant_value[1]
                        object_value = ids.get(referred_name)
                    triples.append((subject, f"mathmoddb:{relation_uri.split('/')[-1]}", object_value))
                    triples.append((object_value, f"mathmoddb:{inversePropertyMapping[relation_uri].split('/')[-1]}", subject))
    
    return triples, ids

def generate_sparql_insert_with_new_ids(triples):
    # Step 1: Identify new items that need mardmo IDs
    new_items = {}
    counter = 0
    for triple in triples:
        subject = triple[0]
        if not subject.startswith("mathmoddb:"):
            # Assign temporary placeholders for new IDs
            new_items[subject] = f"newItem{counter}"
            counter += 1

    # Step 2: Generate SPARQL query with BIND for new mardmo IDs
    insert_query = """
    PREFIX mathmoddb: <https://mardi4nfdi.de/mathmoddb#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
            if obj.startswith('mathmoddb:') or obj.startswith('"') or obj.startswith(':') or obj.startswith('<'):
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
        FILTER (STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathmoddb#mardmo"))
        BIND (xsd:integer(SUBSTR(STR(?id), STRLEN("https://mardi4nfdi.de/mathmoddb#mardmo") + 1)) AS ?num)
      }
    }
    BIND (IF(BOUND(?maxID), ?maxID + 1, 0) AS ?nextID)
    """
    id_counter = 0
    for new_item in new_items:
        insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathmoddb#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        id_counter += 1

    insert_query += "}"

    return insert_query



                    
