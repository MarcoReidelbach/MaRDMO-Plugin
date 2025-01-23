from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option


from .utils import add_basics, add_entity, add_properties, add_relations
from .sparql import queryHandler
from ..utils import get_data, query_sparql, splitVariableText, value_editor
from ..config import BASE_URI
from ..id import *


@receiver(post_save, sender=Value)
def RFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/field/id':
        if instance.text and instance.text != 'not found':
            add_basics(instance, 
                       f'{BASE_URI}domain/field/name', 
                       f'{BASE_URI}domain/field/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['researchFieldInformation'].format(f":{Id}"))
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
                if results:
                    # Add relations of the Research Field to the Questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/field/field-relation', 
                                  f'{BASE_URI}domain/field/field-relatant', 
                                  ['generalizedByField','generalizesField','similarToField'])
                    # Add Publications to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P')
    return

@receiver(post_save, sender=Value)
def RPInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/problem/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}domain/problem/name', 
                       f'{BASE_URI}domain/problem/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['researchProblemInformation'].format(f":{Id}"))
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
                if results:
                    # Add related Research Fields to questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/problem/field-relation',
                                  f'{BASE_URI}domain/problem/field-relatant',
                                  ['containedInField'], 
                                  False, '', None, True)
                    # Add related Research Problems to questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/problem/problem-relation',
                                  f'{BASE_URI}domain/problem/problem-relatant', 
                                  ['generalizedByProblem','generalizesProblem','similarToProblem'])
                    # Add Research Fields to questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/field', 
                               f'{BASE_URI}domain/field/id', 
                               'containedInField', 'RF')
                    # Add Publications to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P')
    return

@receiver(post_save, sender=Value)
def QQKInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/quantity/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}domain/quantity/name', 
                       f'{BASE_URI}domain/quantity/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['quantityOrQuantityKindInformation'].format(f":{Id}"))
                print(results)
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
                if results:
                    # Add Type of Quantity
                    if results[0].get('class',{}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/quantity/is-quantity-or-quantity-kind', None, None, Option.objects.get(uri=mathmoddb[results[0]['class']['value']]), None, 0, instance.set_index)
                    # Add the Quantity Properties to the Questionnaire
                    add_properties(instance, results, mathmoddb, 
                                   f'{BASE_URI}domain/quantity/quantity-properties')
                    # Add the Quantity Kind Properties to the Questionnaire
                    add_properties(instance, results, mathmoddb, 
                                   f'{BASE_URI}domain/quantity/quantity-kind-properties')
                    # Add other References
                    if results[0].get('qudtID',{}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/quantity/reference', results[0]['qudtID']['value'].removeprefix('https://qudt.org/vocab/'), None, Option.objects.get(uri=options['QUDT']), 0, 0, instance.set_index)
                    # Add related quantities or quantity kinds to questionnaire
                    idx_qq = 0; idx_qkqk = 0; idx_qqk = 0; idx_qkq = 0
                    for prop in ['generalizedByQuantity','generalizesQuantity','approximatedByQuantity','approximatesQuantity','linearizedByQuantity',
                                 'linearizesQuantity','nondimensionalizedByQuantity','nondimensionalizesQuantity','similarToQuantity']:
                        if results[0].get(prop, {}).get('value'):
                            for result in results[0][prop]['value'].split(' / '):
                                quantityID, quantityLabel, quantityDescription, quantityClass = result.split(' | ')
                                if results[0]['class']['value'] == 'Quantity' and quantityClass == 'Quantity':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qq, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qq, f"{instance.set_index}|0")
                                    idx_qq +=1
                                elif results[0]['class']['value'] == 'QuantityKind' and quantityClass == 'QuantityKind':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity-kind/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qkqk, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity-kind/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qkqk, f"{instance.set_index}|0")
                                    idx_qkqk +=1
                                elif results[0]['class']['value'] == 'Quantity' and quantityClass == 'QuantityKind':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity-kind/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qqk, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity-kind/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qqk, f"{instance.set_index}|0")
                                    idx_qqk +=1
                                elif results[0]['class']['value'] == 'QuantityKind' and quantityClass == 'Quantity':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qkq, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qkq, f"{instance.set_index}|0")
                                    idx_qkq +=1
                    # Add Publications to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P')
    return

@receiver(post_save, sender=Value)
def MFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/formulation/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}domain/formulation/name', 
                       f'{BASE_URI}domain/formulation/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['mathematicalFormulationInformation'].format(f":{Id}"))
                mathmoddb = get_data('model/data/mapping.json')
                options = get_data('data/options.json')
                if results:
                    # Add the Mathematical Model Properties to the Questionnaire
                    add_properties(instance, results, mathmoddb, 
                                   f'{BASE_URI}domain/formulation/properties')
                    # Add the defined Quantity
                    if results[0].get('defines', {}).get('value',''):
                        value_editor(instance.project, f'{BASE_URI}domain/formulation/is-definition', None, None, Option.objects.get(uri=options['Yes']), None, 0, instance.set_index)
                        mfIDs = results[0]['defines']['value'].split(' / ')
                        mfLabels = results[0]['definesLabel']['value'].split(' / ')
                        mfDescriptions = results[0]['definesDescription']['value'].split(' / ')
                        for mfID, mfLabel, mfDescription in zip(mfIDs, mfLabels, mfDescriptions):
                            value_editor(instance.project, f'{BASE_URI}domain/formulation/defined-quantity', f"{mfLabel} ({mfDescription}) [mathmoddb]", f'mathmoddb:{mfID}', None, None, 0, instance.set_index)
                    else:
                        value_editor(instance.project, f'{BASE_URI}domain/formulation/is-definition', None, None, Option.objects.get(uri=options['No']), None, 0, instance.set_index)
                    # Add the Formula to the Questionnaire
                    if results[0].get('formulas', {}).get('value',''):
                        formulas = results[0]['formulas']['value'].split(' / ')
                        for idx, formula in enumerate(formulas):
                            value_editor(instance.project, f'{BASE_URI}domain/formulation/formula', formula, None, None, idx, 0, instance.set_index)
                    # Add the Elements to the Questionnaire
                    if results[0].get('terms', {}).get('value',''):
                        terms = results[0]['terms']['value'].split(' / ')
                        qIDs = results[0].get('containsQuantity', {}).get('value','').split(' / ')
                        qLabels = results[0].get('containsQuantityLabel', {}).get('value','').split(' / ')
                        qDescriptions = results[0].get('containsQuantityDescription', {}).get('value','').split(' / ')
                        for idx, term in enumerate(terms):
                            symbol, quantity = splitVariableText(term)
                            for qID, qLabel, qDescription in zip(qIDs, qLabels, qDescriptions):
                                if quantity == qLabel:
                                    #value_editor(instance, 'MathematicalFormulation/Element', None, None, None, None, idx, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/formulation/element/symbol', symbol, None, None, None, idx, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/formulation/element/quantity', f"{qLabel} ({qDescription}) [mathmoddb]", f'mathmoddb:{qID}', None, None, idx, f"{instance.set_index}|0")
                    # Add the contained in Model statements
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/formulation/model-relation',
                                  f'{BASE_URI}domain/formulation/model-relatant', 
                                  ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn'],
                                  True, 'MM', f"{instance.set_index}|0")
                    # Add the contained in / contains Formulation statements
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/formulation/formulation-relation-1',
                                  f'{BASE_URI}domain/formulation/formulation-relatant-1', 
                                  ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn','containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition'],
                                  True, 'MF', f"{instance.set_index}|0")
                    # Add relations of the Mathematical Model to the Questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/formulation/formulation-relation-2',
                                  f'{BASE_URI}domain/formulation/formulation-relatant-2', 
                                  ['generalizedByFormulation','generalizesFormulation','discretizedByFormulation','discretizesFormulation','approximatedByFormulation','approximatesFormulation','linearizedByFormulation','linearizesFormulation','nondimensionalizedByFormulation','nondimensionalizesFormulation','similarToFormulation'])
                    # Add Quantities and Quantity Kinds to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/quantity', 
                               f'{BASE_URI}domain/quantity/id', 
                               'containsQuantity', 'QQK')
                    # Add Publications to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P')
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
    if instance and instance.attribute.uri == f'{BASE_URI}domain/model/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            add_basics(instance, 
                       f'{BASE_URI}domain/model/name', 
                       f'{BASE_URI}domain/model/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['mathematicalModelInformation'].format(f":{Id}"))
                mathmoddb = get_data('model/data/mapping.json')
                if results:
                    print(results)
                    # Add the Mathematical Model Properties to the Questionnaire
                    add_properties(instance, results, mathmoddb, 
                                   f'{BASE_URI}domain/model/properties')
                    # Add modeled Research Problems to questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/model/problem-relation', 
                                  f'{BASE_URI}domain/model/problem-relatant', 
                                  ['models'], 
                                  False, '', None, True)
                    
                    # Add related mathematical models to questionnaire
                    add_relations(instance, results, mathmoddb, 
                                  f'{BASE_URI}domain/model/model-relation', 
                                  f'{BASE_URI}domain/model/model-relatant', 
                                  ['generalizedByModel','generalizesModel','discretizedByModel','discretizesModel','containedInModel','containsModel','approximatedByModel','approximatesModel','linearizedByModel','linearizesModel','similarToModel'])
                    # Add Research Problem to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/problem', 
                               f'{BASE_URI}domain/problem/id', 
                               'models', 'RP')
                    # Add Formulation to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/formulation', 
                               f'{BASE_URI}domain/formulation/id', 
                               'formulation', 'MF')
                    # Add Task to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/task', 
                               f'{BASE_URI}domain/task/id', 
                               'appliedByTask', 'T')
                    # Add Publications to Questionnaire
                    add_entity(instance, results, 
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P')
                    
    return

@receiver(post_save, sender=Value)
def RP2RF(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/problem/field-relatant':
        # Load MathModDB Vocabulary
        mathmoddb = get_data('model/data/mapping.json')
        # Add Research Field Relation to questionnaire
        value_editor(instance.project, f'{BASE_URI}domain/problem/field-relation', mathmoddb['containedInField'], None, None, instance.collection_index, 0, instance.set_prefix)
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
def RP2MM(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/model/problem-relatant':
        # Load MathModDB Vocabulary
        mathmoddb = get_data('model/data/mapping.json')
        # Add Model Relation to questionnaire
        value_editor(instance.project, f'{BASE_URI}domain/model/problem-relation', mathmoddb['models'], None, None, instance.collection_index, 0, instance.set_prefix)