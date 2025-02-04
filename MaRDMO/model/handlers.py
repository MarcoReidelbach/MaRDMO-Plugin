from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option


from .utils import add_basics, add_entity, add_properties, add_relations
from .sparql import queryHandler
from .models import ResearchField, ResearchProblem, MathematicalModel, QuantityOrQuantityKind, MathematicalFormulation
from ..utils import add_entities, extract_parts, get_data, get_id, get_questionsMO, query_sparql, splitVariableText, value_editor
from ..config import BASE_URI
from ..id import *


@receiver(post_save, sender=Value)
def RFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Model Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Field ID"]["uri"]}':
        if instance.text and instance.text != 'not found':
            add_basics(instance, 
                       f'{BASE_URI}{questions["Research Field Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Research Field Description"]["uri"]}')
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
                    props = ['generalizedByField', 'generalizesField', 'similarToField']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Research Field IntraClassRelation"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[prop]), 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Research Field IntraClassElement"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            idx +=1
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
    # Get Questions of Model Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Problem ID"]["uri"]}':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}{questions["Research Problem Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Research Problem Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['researchProblemInformation'].format(Id))
                mathmoddb = get_data('model/data/mapping.json')
                if results:
                    # Structure Results
                    data = ResearchProblem.from_query(results)
                    # Add Research Fields to Questionnaire
                    for idx, field in enumerate(data.containedInField):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Research Problem RFRelatant"]["uri"]}', 
                                     text = f"{field.label} ({field.description}) [{source}]", 
                                     external_id = field.id, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Relations between Research Problems to Questionnaire
                    props = ['generalizedByProblem', 'generalizesProblem', 'similarToProblem']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Research Problem IntraClassRelation"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[prop]), 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Research Problem IntraClassElement"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            idx +=1
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
    # Get Questions of Model Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Quantity ID"]["uri"]}':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}{questions["Quantity Name"]["uri"]}',
                       f'{BASE_URI}{questions["Quantity Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['quantityOrQuantityKindInformation'].format(Id))
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
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
                        for key, property in data.properties.items():
                            value_editor(project = instance.project, 
                                         uri  = f'{BASE_URI}{questions["Quantity QProperties"]["uri"]}', 
                                         option = Option.objects.get(uri=property), 
                                         collection_index = key,
                                         set_index = 0, 
                                         set_prefix = instance.set_index)
                    elif data.qclass == 'QuantityKind':
                        for key, property in data.properties.items():
                            value_editor(project = instance.project, 
                                         uri  = f'{BASE_URI}{questions["Quantity QKProperties"]["uri"]}', 
                                         option = Option.objects.get(uri=property), 
                                         collection_index = key,
                                         set_index = 0, 
                                         set_prefix = instance.set_index)
                    # Add ofther References (QUDT ID)
                    if data.qudtID:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Quantity Reference"]["uri"]}', 
                                     text = data.qudtID, 
                                     option = Option.objects.get(uri=options['QUDT']), 
                                     collection_index = 0, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Relations between Quantities and Quantity Kinds to Questionnaire
                    props = ['generalizedByQuantity','generalizesQuantity','approximatedByQuantity','approximatesQuantity','linearizedByQuantity','linearizesQuantity','nondimensionalizedByQuantity','nondimensionalizesQuantity','similarToQuantity']
                    idx_qq = 0; idx_qkqk = 0; idx_qqk = 0; idx_qkq = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            if data.qclass == 'Quantity' and value.qclass == 'Quantity':
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["Quantity Q2Q"]["uri"]}', 
                                             option = Option.objects.get(uri=mathmoddb[prop]), 
                                             set_index = idx_qq, 
                                             set_prefix = f"{instance.set_index}|0")
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["Quantity QRelatant"]["uri"]}', 
                                             text = f"{value.label} ({value.description}) [{source}]", 
                                             external_id = value.id, 
                                             set_index = idx_qq, 
                                             set_prefix = f"{instance.set_index}|0")
                                idx_qq +=1
                            elif data.qclass == 'QuantityKind' and value.qclass == 'QuantityKind':
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["QuantityKind QK2QK"]["uri"]}', 
                                             option = Option.objects.get(uri=mathmoddb[prop]), 
                                             set_index = idx_qkqk, 
                                             set_prefix = f"{instance.set_index}|0")
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["QuantityKind QKRelatant"]["uri"]}', 
                                             text = f"{value.label} ({value.description}) [{source}]", 
                                             external_id = value.id, 
                                             set_index = idx_qkqk, 
                                             set_prefix = f"{instance.set_index}|0")
                                idx_qkqk +=1
                            elif data.qclass == 'Quantity' and value.qclass == 'QuantityKind':
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["Quantity Q2QK"]["uri"]}', 
                                             option = Option.objects.get(uri=mathmoddb[prop]), 
                                             set_index = idx_qqk, 
                                             set_prefix = f"{instance.set_index}|0")
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["Quantity QKRelatant"]["uri"]}', 
                                             text = f"{value.label} ({value.description}) [{source}]", 
                                             external_id = value.id, 
                                             set_index = idx_qqk, 
                                             set_prefix = f"{instance.set_index}|0")
                                idx_qqk +=1
                            elif data.qclass == 'QuantityKind' and value.qclass == 'Quantity':
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["QuantityKind QK2Q"]["uri"]}', 
                                             option = Option.objects.get(uri=mathmoddb[prop]), 
                                             set_index = idx_qkq, 
                                             set_prefix = f"{instance.set_index}|0")
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions["QuantityKind QRelatant"]["uri"]}', 
                                             text = f"{value.label} ({value.description}) [{source}]", 
                                             external_id = value.id, 
                                             set_index = idx_qkq, 
                                             set_prefix = f"{instance.set_index}|0")
                                idx_qkq +=1
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
    # Get Questions of Model Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}{questions["Mathematical Formulation Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Mathematical Formulation Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['mathematicalFormulationInformation'].format(Id))
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
                if results:
                    data = MathematicalFormulation.from_query(results)
                    # Add the Mathematical Formulation Properties to the Questionnaire
                    for key, property in data.properties.items():
                        value_editor(project = instance.project, 
                                     uri  = f'{BASE_URI}{questions["Mathematical Formulation Properties"]["uri"]}', 
                                     option = Option.objects.get(uri=property), 
                                     collection_index = key,
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add the defined Quantity
                    if data.defines:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Mathematical Formulation Definition"]["uri"]}', 
                                     option = Option.objects.get(uri=options['Yes']), 
                                     set_index = 0, 
                                     set_prefix =instance.set_index)
                        for quantity in data.defines:
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation Defined Quantity"]["uri"]}', 
                                         text = f"{quantity.label} ({quantity.description}) [{source}]", 
                                         external_id = quantity.id, 
                                         set_index = 0, 
                                         set_prefix = instance.set_index)
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
                    props = ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, f"{prop}MM"):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation MF2MM"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[prop]), 
                                         set_index = idx, 
                                         set_prefix = f"{instance.set_index}|0")
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation MMRelatant"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = f"{instance.set_index}|0")
                            idx +=1

                    # Add Relations between Formulations I
                    props = ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn','containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, f"{prop}MF"):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation MF2MF"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[prop]), 
                                         set_index = idx, 
                                         set_prefix = f"{instance.set_index}|0")
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation MFRelatant"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = f"{instance.set_index}|0")
                            idx +=1
                    # Add relations of the Mathematical Model to the Questionnaire
                    props = ['generalizedByFormulation','generalizesFormulation','discretizedByFormulation','discretizesFormulation','approximatedByFormulation','approximatesFormulation','linearizedByFormulation','linearizesFormulation','nondimensionalizedByFormulation','nondimensionalizesFormulation','similarToFormulation']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation IntraClassRelation"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[prop]), 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Formulation IntraClassElement"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            idx +=1
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
    if instance and instance.attribute.uri == f'{BASE_URI}domain/task/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}domain/task/name', 
                       f'{BASE_URI}domain/task/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['taskInformation'].format(f":{Id}"))
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
                if results:
                    # Add the Task Properties to the Questionnaire
                    add_properties(instance, results, mathmoddb, 
                                   f'{BASE_URI}domain/task/properties')
                    # Add the Category to the Questionnaire
                    value_editor(instance.project, f'{BASE_URI}domain/task/category', None, None, Option.objects.get(uri=mathmoddb['ComputationalTask']), None, 0, instance.set_index)
                    # Add applied Model to the Questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/task/model-relation', 
                                  f'{BASE_URI}domain/task/model-relatant', 
                                  ['appliesModel'], 
                                  False, '', None, True)
                    # Add Formulations contained in Task
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/task/formulation-relation', 
                                  f'{BASE_URI}domain/task/formulation-relatant', 
                                  ['containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition'],
                                  True, '', f"{instance.set_index}|0")
                    # Add Quantity contained in Task
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/task/quantity-relation', 
                                  f'{BASE_URI}domain/task/quantity-relatant', 
                                  ['containsInput','containsOutput','containsObjective','containsParameter','containsConstant'],
                                  True, '', f"{instance.set_index}|0")
                    # Add related Task to questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/task/task-relation', 
                                  f'{BASE_URI}domain/task/task-relatant', 
                                  ['generalizedByTask','generalizesTask','discretizedByTask','discretizesTask','containedInTask','containsTask','approximatedByTask','approximatesTask','linearizedByTask','linearizesTask','similarToTask'])
                    # Add Quantities and Quantity Kinds to Questionnaire
                    for prop in ['containsInput','containsOutput','containsObjective','containsParameter','containsConstant']:
                        add_entity(instance, results, 
                                   f'{BASE_URI}domain/quantity', 
                                   f'{BASE_URI}domain/quantity/id', 
                                   prop, 'QQK')
                    # Add Formulations to Questionnaire
                    for prop in ['containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition']:
                        add_entity(instance, results, 
                                   f'{BASE_URI}domain/formulation', 
                                   f'{BASE_URI}domain/formulation/id', 
                                   prop, 'MF')
                    # Add Publications to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P')
    return                    

@receiver(post_save, sender=Value)
def MMInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Model Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Model ID"]["uri"]}':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}{questions["Mathematical Model Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Mathematical Model Description"]["uri"]}')
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
                    for key, property in data.properties.items():
                        value_editor(project = instance.project, 
                                     uri  = f'{BASE_URI}{questions["Mathematical Model Properties"]["uri"]}', 
                                     option = Option.objects.get(uri=property), 
                                     collection_index = key,
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Research Problem to Questionnaire
                    for idx, problem in enumerate(data.models):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Mathematical Model RPRelatant"]["uri"]}', 
                                     text = f"{problem.label} ({problem.description}) [{source}]", 
                                     external_id = problem.id, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Relations between Research Fields to Questionnaire
                    props = ['generalizedByModel','generalizesModel','discretizedByModel','discretizesModel','containedInModel','containsModel','approximatedByModel','approximatesModel','linearizedByModel','linearizesModel','similarToModel']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Model IntraClassRelation"]["uri"]}', 
                                         option = Option.objects.get(uri=mathmoddb[prop]), 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Mathematical Model IntraClassElement"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            idx +=1
                    # Add Formulation to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
                                 datas = data.appliedByTask, 
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
def RP2RF(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsMO()
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
                ID = instance.external_id
                # Get (set) ids of exisitng research field in questionnaire
                set_ids = get_id(instance.project, f'{BASE_URI}{questions["Research Field"]["uri"]}', ['set_index'])
                value_ids = get_id(instance.project, f'{BASE_URI}{questions["Research Field ID"]["uri"]}', ['external_id'])
                # Add Research Field entry to questionnaire
                idx = max(set_ids, default = -1) + 1
                if ID not in value_ids:
                    # Set up Page
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Research Field"]["uri"]}', 
                                 text = f"RF{idx}", 
                                 set_index = idx)
                    # Add ID Values
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Research Field ID"]["uri"]}', 
                                 text = f'{label} ({description}) [{source}]', 
                                 external_id = ID, 
                                 set_index = idx)
                    idx += 1
                    value_ids.append(ID)
    return

@receiver(post_save, sender=Value)
def T2MM(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/task/model-relatant':
        # Load MathModDB Vocabulary
        mathmoddb = get_data('model/data/mapping.json')
        # Add Model Relation to questionnaire
        value_editor(instance.project, f'{BASE_URI}domain/task/model-relation', mathmoddb['appliesModel'], None, None, instance.collection_index, 0, instance.set_prefix)

@receiver(post_save, sender=Value)
def QQK2MF(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Model Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Formulation Element Quantity"]["uri"]}':
        label, description, source =  extract_parts(instance.text)
        if source != 'user':
                ID = instance.external_id
                # Get (set) ids of exisitng research problem in questionnaire
                set_ids = get_id(instance.project, f'{BASE_URI}{questions["Quantity"]["uri"]}', ['set_index'])
                value_ids = get_id(instance.project, f'{BASE_URI}{questions["Quantity ID"]["uri"]}', ['external_id'])
                # Add Research Field entry to questionnaire
                idx = max(set_ids, default = -1) + 1
                if ID not in value_ids:
                    # Set up Page
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Quantity"]["uri"]}', 
                                 text = f"QQK{idx}", 
                                 set_index = idx)
                    # Add ID Values
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Quantity ID"]["uri"]}', 
                                 text = f'{label} ({description}) [{source}]', 
                                 external_id = ID, 
                                 set_index = idx)
                    idx += 1
                    value_ids.append(ID)


@receiver(post_save, sender=Value)
def RP2MM(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsMO()
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Model RPRelatant"]["uri"]}':
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
                ID = instance.external_id
                # Get (set) ids of exisitng research problem in questionnaire
                set_ids = get_id(instance.project, f'{BASE_URI}{questions["Research Problem"]["uri"]}', ['set_index'])
                value_ids = get_id(instance.project, f'{BASE_URI}{questions["Research Problem ID"]["uri"]}', ['external_id'])
                # Add Research Field entry to questionnaire
                idx = max(set_ids, default = -1) + 1
                if ID not in value_ids:
                    # Set up Page
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Research Problem"]["uri"]}', 
                                 text = f"RF{idx}", 
                                 set_index = idx)
                    # Add ID Values
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Research Problem ID"]["uri"]}', 
                                 text = f'{label} ({description}) [{source}]', 
                                 external_id = ID, 
                                 set_index = idx)
                    idx += 1
                    value_ids.append(ID)
