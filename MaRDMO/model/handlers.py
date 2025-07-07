from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option

from .constants import PROPS, RELATANT_URIS, RELATION_URIS, INDEX_COUNTERS, get_URI_PREFIX_MAP
from .sparql import queryHandler
from .models import ResearchField, ResearchProblem, MathematicalModel, QuantityOrQuantityKind, MathematicalFormulation, Task, Relatant

from ..id_staging import ITEMS, PROPERTIES
from ..utils import add_basics, add_entities, add_new_entities, add_properties, add_relations, add_references, extract_parts, get_mathmoddb, get_questionsMO, get_questionsPU, query_sparql, value_editor
from ..config import BASE_URI, endpoint


@receiver(post_save, sender=Value)
def RFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO() | get_questionsPU()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Field ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Research Field Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Research Field Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['researchFieldInformation'].format(Id, f"{endpoint[source]['uri']}/entity/", **ITEMS, **PROPERTIES)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    # Structure Results
                    data = ResearchField.from_query(results)
                    # Add Optional Long Descriptions
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Research Field Long Description"]["uri"]}', 
                                         text = descriptionLong, 
                                         collectionn_index = idx,
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                    # Add Relations between Research Fields to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Field'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Research Field IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Research Field IntraClassRelation"]["uri"]}')
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def RPInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO() | get_questionsPU()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Problem ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                # Get Label and Description of Item and add to questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Research Problem Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Research Problem Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['researchProblemInformation'].format(Id, **ITEMS, **PROPERTIES)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    # Structure Results
                    data = ResearchProblem.from_query(results)
                    # Add Optional Long Description
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Research Problem Long Description"]["uri"]}', 
                                         text = descriptionLong,
                                         collection_index = idx, 
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                    # Add Relations between Research Problem and Research Fields to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['RP2RF'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Research Problem RFRelatant"]["uri"]}')
                    # Add Relations between Research Problems to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Problem'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Research Problem IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Research Problem IntraClassRelation"]["uri"]}')
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')                
    return

@receiver(post_save, sender=Value)
def QQKInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO() | get_questionsPU()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Quantity ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                # Get Label and Description of Item and add to questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Quantity Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Quantity Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                print(instance.external_id)
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['quantityOrQuantityKindInformation'].format(Id, **ITEMS, **PROPERTIES)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    # Structure Results
                    data = QuantityOrQuantityKind.from_query(results)
                    # Add Optional Long Description
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Quantity Long Description"]["uri"]}', 
                                         text = descriptionLong,
                                         collection_index = idx, 
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                    # Add Type of Quantity
                    if data.qclass:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Quantity QorQK"]["uri"]}', 
                                     option = Option.objects.get(uri=mathmoddb[results[0]['class']['value']]),
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Properties to the Questionnaire
                    add_properties(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Quantity Properties"]["uri"]}',
                                   set_prefix = instance.set_index)
                    # Add References to the Questionnaire
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Quantity Reference"]["uri"]}',
                                   set_prefix = instance.set_index)
                    # Add the Formula to the Questionnaire
                    for idx, formula in enumerate(data.formulas):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Quantity Formula"]["uri"]}', 
                                     text = formula, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix =instance.set_index)
                    # Add the Symbols to the Questionnaire
                    for idx, symbol in enumerate(data.symbols):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Quantity Element Symbol"]["uri"]}', 
                                     text = symbol, 
                                     set_index = idx, 
                                     set_prefix = f"{instance.set_index}|0")
                    # Add the Quantities to the Questionnaire
                    for idx, quantity in enumerate(data.containsQuantity):
                        source, _ = quantity.id.split(':')
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Quantity Element Quantity"]["uri"]}', 
                                     text = f"{quantity.label} ({quantity.description}) [{source}]", 
                                     external_id = quantity.id, 
                                     set_index = idx, 
                                     set_prefix = f"{instance.set_index}|0")
                    # Add Relations between Quantities and Quantity Kinds to Questionnaire
                    for prop in PROPS['Quantity']:
                        for value in getattr(data, prop):
                            qclass_pair = (data.qclass, value.qclass)
                            value_editor(
                                project=instance.project,
                                uri=f"{BASE_URI}{questions[RELATION_URIS[qclass_pair]]['uri']}",
                                option=Option.objects.get(uri=mathmoddb[prop]),
                                set_index=INDEX_COUNTERS[qclass_pair],
                                set_prefix=f"{instance.set_index}"
                            )
                            value_editor(
                                project=instance.project,
                                uri=f"{BASE_URI}{questions[RELATANT_URIS[qclass_pair]]['uri']}",
                                text=f"{value.label} ({value.description}) [{source}]",
                                external_id=value.id,
                                set_index=INDEX_COUNTERS[qclass_pair],
                                set_prefix=f"{instance.set_index}"
                            )
                            INDEX_COUNTERS[qclass_pair] += 1
                    
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')   
    return

@receiver(post_save, sender=Value)
def MFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO() | get_questionsPU()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                # Get Label and Description of Item and add to questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Mathematical Formulation Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Mathematical Formulation Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )# Get source and ID of Item
                print(instance.external_id)
                source, Id = instance.external_id.split(':')

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['mathematicalFormulationInformation'].format(Id, **ITEMS, **PROPERTIES)
                results = query_sparql(query, endpoint[source]['sparql'])
                print(results)
                mathmoddb = get_mathmoddb()
                
                if results:
                    # Structure Results
                    data = MathematicalFormulation.from_query(results)
                    print(data)
                    # Add Optional Long Description
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation Long Description"]["uri"]}', 
                                         text = descriptionLong,
                                         collection_index = idx, 
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                    # Add Properties to the Questionnaire
                    add_properties(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Mathematical Formulation Properties"]["uri"]}',
                                   set_prefix = instance.set_index)
                    # Add the Formula to the Questionnaire
                    for idx, formula in enumerate(data.formulas):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Mathematical Formulation Formula"]["uri"]}', 
                                     text = formula, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix =instance.set_index)
                    # Add the Symbols to the Questionnaire
                    for idx, symbol in enumerate(data.symbols):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Mathematical Formulation Element Symbol"]["uri"]}', 
                                     text = symbol, 
                                     set_index = idx, 
                                     set_prefix = f"{instance.set_index}|0")
                    # Add the Quantities to the Questionnaire
                    for idx, quantity in enumerate(data.containsQuantity):
                        source, _ = quantity.id.split(':')
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Mathematical Formulation Element Quantity"]["uri"]}', 
                                     text = f"{quantity.label} ({quantity.description}) [{source}]", 
                                     external_id = quantity.id, 
                                     set_index = idx, 
                                     set_prefix = f"{instance.set_index}|0")
                    # Add Relations between Formulations I
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['MF2MF'], 
                                  mapping = mathmoddb, 
                                  set_prefix = f"{instance.set_index}|0",
                                  relatant = f'{BASE_URI}{questions["Mathematical Formulation MFRelatant"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Mathematical Formulation MF2MF"]["uri"]}')
                    # Add Relations between Formulations II to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Formulation'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Mathematical Formulation IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Mathematical Formulation IntraClassRelation"]["uri"]}',
                                  assumption = f'{BASE_URI}{questions["Mathematical Formulation Assumption"]["uri"]}')
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')                
    return

@receiver(post_save, sender=Value)
def TInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO() | get_questionsPU()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Task ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                # Get Label and Description of Item and add to questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Task Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Task Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['taskInformation'].format(Id, **ITEMS, **PROPERTIES)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    #Structure Results
                    data = Task.from_query(results)
                    
                    # Add Optional Long Description
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Task Long Description"]["uri"]}', 
                                         text = descriptionLong, 
                                         collection_index = idx,
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                    # Add properties to the Questionnaire
                    add_properties(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Task Properties"]["uri"]}',
                                   set_prefix = instance.set_index)
                    # Add Formulations contained in Task
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['T2MF'], 
                                  mapping = mathmoddb, 
                                  set_prefix = f"{instance.set_index}|0",
                                  relatant = f'{BASE_URI}{questions["Task MFRelatant"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Task T2MF"]["uri"]}')
                    # Add Quantity contained in Task
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['T2Q'], 
                                  mapping = mathmoddb, 
                                  set_prefix = f"{instance.set_index}|0",
                                  relatant = f'{BASE_URI}{questions["Task QRelatant"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Task T2Q"]["uri"]}')
                    # Add related Task to questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Task'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index,
                                  relatant = f'{BASE_URI}{questions["Task IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Task IntraClassRelation"]["uri"]}',
                                  assumption = f'{BASE_URI}{questions["Task Assumption"]["uri"]}',
                                  order = f'{BASE_URI}{questions["Task Order Number"]["uri"]}')
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return                    

@receiver(post_save, sender=Value)
def MMInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO() | get_questionsPU()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Model ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                # Get Label and Description of Item and add to questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Mathematical Model Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Mathematical Model Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['mathematicalModelInformation'].format(Id, **ITEMS, **PROPERTIES)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                if results:
                    # Structure Results
                    data = MathematicalModel.from_query(results)
                    
                    # Add Optional Long Description
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Model Long Description"]["uri"]}', 
                                         text = descriptionLong,
                                         collection_index = idx, 
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                    # Add the Mathematical Model Properties to the Questionnaire
                    add_properties(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Mathematical Model Properties"]["uri"]}',
                                   set_prefix = instance.set_index)
                    
                    # Add Relations between Mathematical Models and Research Problems to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['MM2RP'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Mathematical Model RPRelatant"]["uri"]}')
                    
                    # Add Formulations contained in Mathematical Model
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['MM2MF'], 
                                  mapping = mathmoddb, 
                                  set_prefix = f"{instance.set_index}|0",
                                  relatant = f'{BASE_URI}{questions["Mathematical Model MFRelatant"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Mathematical Model MM2MF"]["uri"]}',
                                  order = f'{BASE_URI}{questions["Mathematical Model Order Number"]["uri"]}')
                    
                    # Add Relations between Mathematical Models and Tasks to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['MM2T'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Mathematical Model TRelatant"]["uri"]}')
                    
                    # Add related Models to questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Model'], 
                                  mapping = mathmoddb, 
                                  set_prefix = instance.set_index,
                                  relatant = f'{BASE_URI}{questions["Mathematical Model IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Mathematical Model IntraClassRelation"]["uri"]}',
                                  assumption = f'{BASE_URI}{questions["Mathematical Model Assumption"]["uri"]}')
                    
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')                   
    return

@receiver(post_save, sender=Value)
def RelationHandler(sender, **kwargs):
    
    #Get Instance
    instance = kwargs.get("instance", None)
    
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':

        # Get config map
        config_map = get_URI_PREFIX_MAP()

        if instance.attribute.uri in config_map and instance.text:

            # Get item, config and data information
            label, description, source = extract_parts(instance.text)
            config = config_map[instance.attribute.uri]
            datas = [Relatant.from_relation(instance.external_id, label, description)]

            # Add items from specific source
            if source != 'user':
                add_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    question_id=config["question_id"],
                    datas=datas,
                    source=source,
                    prefix=config["prefix"]
                )
            
            # Add items from user
            elif instance.external_id == 'not found':
                add_new_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    question_id=config["question_id"],
                    datas=datas,
                    source=source,
                    prefix=config["prefix"]
                )

    return
