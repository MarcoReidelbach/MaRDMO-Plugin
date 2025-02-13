from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option

from .constants import PROPS, RELATANT_URIS, RELATION_URIS, INDEX_COUNTERS
from .sparql import queryHandler
from .models import ResearchField, ResearchProblem, MathematicalModel, QuantityOrQuantityKind, MathematicalFormulation, Task, Relatant

from ..utils import add_basics, add_entities, add_properties, add_relations, add_references, extract_parts, get_data, get_questionsMO, query_sparql, splitVariableText, value_editor
from ..config import BASE_URI


@receiver(post_save, sender=Value)
def RFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questionsMO()
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
                if source== 'mathmoddb':
                    # If Item from MathModDB, query relations and load MathModDB Vocabulary
                    results = query_sparql(queryHandler['researchFieldInformation'].format(Id))
                    mathmoddb = get_data('model/data/mapping.json')
                    if results:
                        # Structure Results
                        data = ResearchField.from_query(results)
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
        questions = get_questionsMO()
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
                if source== 'mathmoddb':
                    # If Item from MathModDB, query relations and load MathModDB Vocabulary
                    results = query_sparql(queryHandler['researchProblemInformation'].format(Id))
                    mathmoddb = get_data('model/data/mapping.json')
                    if results:
                        # Structure Results
                        data = ResearchProblem.from_query(results)
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
        questions = get_questionsMO()
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
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                if source== 'mathmoddb':
                    # If Item from MathModDB, query relations and load MathModDB Vocabulary
                    results = query_sparql(queryHandler['quantityOrQuantityKindInformation'].format(Id))
                    mathmoddb = get_data('model/data/mapping.json')
                    if results:
                        # Structure Results
                        data = QuantityOrQuantityKind.from_query(results)
                        # Add Type of Quantity
                        if data.qclass:
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Quantity QorQK"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[results[0]['class']['value']]),
                                         set_index = 0, 
                                         set_prefix = instance.set_index)

                        # Add the Quantity or QuantityKind Properties to the Questionnaire
                        if data.qclass == 'Quantity':
                            add_properties(project = instance.project,
                                           data = data,
                                           uri = f'{BASE_URI}{questions["Quantity QProperties"]["uri"]}',
                                           set_prefix = instance.set_index)
                        elif data.qclass == 'QuantityKind':
                            add_properties(project = instance.project,
                                           data = data,
                                           uri = f'{BASE_URI}{questions["Quantity QKProperties"]["uri"]}',
                                           set_prefix = instance.set_index)

                        # Add References to the Questionnaire
                        add_references(project = instance.project,
                                       data = data,
                                       uri = f'{BASE_URI}{questions["Quantity Reference"]["uri"]}',
                                       set_prefix = instance.set_index)

                        # Add Relations between Quantities and Quantity Kinds to Questionnaire
                        for prop in PROPS['Quantity']:
                            for value in getattr(data, prop):
                                qclass_pair = (data.qclass, value.qclass)

                                value_editor(
                                    project=instance.project,
                                    uri=f"{BASE_URI}{questions[RELATION_URIS[qclass_pair]]['uri']}",
                                    option=Option.objects.get(uri=mathmoddb[prop]),
                                    set_index=INDEX_COUNTERS[qclass_pair],
                                    set_prefix=f"{instance.set_index}|0"
                                )

                                value_editor(
                                    project=instance.project,
                                    uri=f"{BASE_URI}{questions[RELATANT_URIS[qclass_pair]]['uri']}",
                                    text=f"{value.label} ({value.description}) [{source}]",
                                    external_id=value.id,
                                    set_index=INDEX_COUNTERS[qclass_pair],
                                    set_prefix=f"{instance.set_index}|0"
                                )

                                INDEX_COUNTERS[qclass_pair] += 1

                        # Add Formulations to Questionnaire
                        add_entities(project = instance.project, 
                                     question_set = f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
                                     question_id = f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
                                     datas = data.definedBy, 
                                     source = source,
                                     prefix = 'MF')            

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
        questions = get_questionsMO()
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
                source, Id = instance.external_id.split(':')
                if source== 'mathmoddb':
                    # If Item from MathModDB, query relations and load MathModDB Vocabulary
                    results = query_sparql(queryHandler['mathematicalFormulationInformation'].format(Id))
                    mathmoddb = get_data('model/data/mapping.json')
                    options = get_data('data/options.json')
                    if results:
                        # Structure Results
                        data = MathematicalFormulation.from_query(results)

                        # Add Properties to the Questionnaire
                        add_properties(project = instance.project,
                                       data = data,
                                       uri = f'{BASE_URI}{questions["Mathematical Formulation Properties"]["uri"]}',
                                       set_prefix = instance.set_index)

                        # Add the defined Quantity
                        if data.defines:
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation Definition"]["uri"]}', 
                                         option = Option.objects.get(uri=options['Yes']), 
                                         set_index = 0, 
                                         set_prefix =instance.set_index)
                            add_relations(project = instance.project, 
                                          data = data, 
                                          props = PROPS['Q2MF'], 
                                          mapping = mathmoddb, 
                                          set_prefix = instance.set_index, 
                                          relatant = f'{BASE_URI}{questions["Mathematical Formulation Defined Quantity"]["uri"]}')
                        else:
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation Definition"]["uri"]}', 
                                         option = Option.objects.get(uri=options['No']), 
                                         set_index = 0, 
                                         set_prefix = instance.set_index)

                        # Add the Formula to the Questionnaire
                        for idx, formula in enumerate(data.formulas):
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["Mathematical Formulation Formula"]["uri"]}', 
                                             text = formula, 
                                             collection_index = idx, 
                                             set_index = 0, 
                                             set_prefix =instance.set_index)

                        # Add the Formula Elements to the Questionnaire
                        for idx, term in enumerate(data.terms):
                            symbol, quantityLabel = splitVariableText(term)
                            for quantity in data.containsQuantity:
                                if quantityLabel == quantity.label:
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Mathematical Formulation Element Symbol"]["uri"]}', 
                                                 text = symbol, 
                                                 set_index = idx, 
                                                 set_prefix = f"{instance.set_index}|0")
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Mathematical Formulation Element Quantity"]["uri"]}', 
                                                 text = f"{quantity.label} ({quantity.description}) [{source}]", 
                                                 external_id = quantity.id, 
                                                 set_index = idx, 
                                                 set_prefix = f"{instance.set_index}|0")

                        # Add Relations between Formulations and Models
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['MF2MM'], 
                                      mapping = mathmoddb, 
                                      set_prefix = f"{instance.set_index}|0",
                                      suffix = 'MM', 
                                      relatant = f'{BASE_URI}{questions["Mathematical Formulation MMRelatant"]["uri"]}', 
                                      relation = f'{BASE_URI}{questions["Mathematical Formulation MF2MM"]["uri"]}')

                        # Add Relations between Formulations I
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['MF2MF'], 
                                      mapping = mathmoddb, 
                                      set_prefix = f"{instance.set_index}|0",
                                      suffix = 'MF', 
                                      relatant = f'{BASE_URI}{questions["Mathematical Formulation MFRelatant"]["uri"]}', 
                                      relation = f'{BASE_URI}{questions["Mathematical Formulation MF2MF"]["uri"]}')

                        # Add Relations between Formulations II to Questionnaire
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['Formulation'], 
                                      mapping = mathmoddb, 
                                      set_prefix = instance.set_index, 
                                      relatant = f'{BASE_URI}{questions["Mathematical Formulation IntraClassElement"]["uri"]}', 
                                      relation = f'{BASE_URI}{questions["Mathematical Formulation IntraClassRelation"]["uri"]}')

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
        questions = get_questionsMO()
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
                if source== 'mathmoddb':
                    # If Item from MathModDB, query relations and load MathModDB Vocabulary
                    results = query_sparql(queryHandler['taskInformation'].format(Id))
                    mathmoddb = get_data('model/data/mapping.json')
                    if results:
                        #Structure Results
                        data = Task.from_query(results)

                        # Add roperties to the Questionnaire
                        add_properties(project = instance.project,
                                       data = data,
                                       uri = f'{BASE_URI}{questions["Task Properties"]["uri"]}',
                                       set_prefix = instance.set_index)

                        # Add the Category to the Questionnaire
                        if data.subclass:
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Task Subclass"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[data.subclass]), 
                                         set_index =  0, 
                                         set_prefix = instance.set_index)

                        # Add applied Models to Questionnaire
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['T2MM'], 
                                      mapping = mathmoddb, 
                                      set_prefix = instance.set_index,
                                      relatant = f'{BASE_URI}{questions["Task MMRelatant"]["uri"]}')

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
                                      relation = f'{BASE_URI}{questions["Task IntraClassRelation"]["uri"]}')

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
        questions = get_questionsMO()
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
                if source== 'mathmoddb':
                    # If Item from MathModDB, query relations and load MathModDB Vocabulary
                    results = query_sparql(queryHandler['mathematicalModelInformation'].format(Id))
                    mathmoddb = get_data('model/data/mapping.json')
                    if results:
                        # Structure Results
                        data = MathematicalModel.from_query(results)

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

                        # Add related Models to questionnaire
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['Model'], 
                                      mapping = mathmoddb, 
                                      set_prefix = instance.set_index,
                                      relatant = f'{BASE_URI}{questions["Mathematical Model IntraClassElement"]["uri"]}', 
                                      relation = f'{BASE_URI}{questions["Mathematical Model IntraClassRelation"]["uri"]}')

                        # Add Formulation to Questionnaire
                        add_entities(project = instance.project, 
                                     question_set = f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
                                     question_id = f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
                                     datas = data.formulation, 
                                     source = source,
                                     prefix = 'MF')

                        # Add Task to Questionnaire
                        add_entities(project = instance.project, 
                                     question_set = f'{BASE_URI}{questions["Task"]["uri"]}',
                                     question_id = f'{BASE_URI}{questions["Task ID"]["uri"]}',
                                     datas = data.appliedByTask, 
                                     source = source,
                                     prefix = 'T')

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
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsMO()
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Research Problem - Research Field Relation
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Problem RFRelatant"]["uri"]}':
            # Check if actual Research Field chosen
            if instance.text:
                # Load MathModDB Vocabulary
                mathmoddb = get_data('model/data/mapping.json')
                label, description, source =  extract_parts(instance.text)
                # Add Research Field Relation to questionnaire
                value_editor(project = instance.project, 
                             uri = f'{BASE_URI}{questions["Research Problem RP2RF"]["uri"]}', 
                             text = mathmoddb['containedInField'],
                             collection_index = instance.collection_index, 
                             set_index = 0, 
                             set_prefix = instance.set_prefix)
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Research Field"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Research Field ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "RF")
        # Task - Mathematical Model Relation
        elif instance.attribute.uri == f'{BASE_URI}{questions["Task MMRelatant"]["uri"]}':
            # Load MathModDB Vocabulary
            mathmoddb = get_data('model/data/mapping.json')
            # Add Model Relation to questionnaire
            value_editor(project = instance.project, 
                         uri = f'{BASE_URI}{questions["Task T2MM"]["uri"]}', 
                         text = mathmoddb['appliesModel'], 
                         collection_index = instance.collection_index, 
                         set_index = 0, 
                         set_prefix = instance.set_prefix)
        # Task - Quantity Relation
        elif instance.attribute.uri == f'{BASE_URI}{questions["Task QRelatant"]["uri"]}':
            label, description, source =  extract_parts(instance.text)
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Quantity"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Quantity ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "QQK")
        # Task - Mathematical Formulation Relation
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Task MFRelatant"]["uri"]}':
            label, description, source =  extract_parts(instance.text)
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "MF")
        # Mathematical Formulation Element
        elif instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Formulation Element Quantity"]["uri"]}':
            label, description, source =  extract_parts(instance.text)
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Quantity"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Quantity ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "QQK")
        # Mathematical Model - Research Problem Relation
        elif instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Model RPRelatant"]["uri"]}':
            # Check if actual Research Problem chosen
            if instance.text:
                # Load MathModDB Vocabulary
                mathmoddb = get_data('model/data/mapping.json')
                label, description, source =  extract_parts(instance.text)
                # Add Research Problem Relation to questionnaire
                value_editor(project = instance.project, 
                             uri = f'{BASE_URI}{questions["Mathematical Model MM2RP"]["uri"]}', 
                             text = mathmoddb['models'],
                             collection_index = instance.collection_index, 
                             set_index = 0, 
                             set_prefix = instance.set_prefix)
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Research Problem"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Research Problem ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "RP")
    return