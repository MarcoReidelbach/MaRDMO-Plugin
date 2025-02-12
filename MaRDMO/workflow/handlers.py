from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value

from ..id import *
from ..config import BASE_URI, mardi_endpoint, wd, wdt, wikidata_endpoint
from ..utils import add_basics, add_entities, add_relations, get_data, get_questionsWO, extract_parts, value_editor, query_sparql

#from .utils import add_basics #, add_entity
from .sparql import mardiProvider, wikidataProvider
from .models import ProcessStep, Relatant
from .constants import PROPS

@receiver(post_save, sender=Value)
def ProgrammingLanguage(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/software/programming-language/id':
        add_basics(instance,
                   f'{BASE_URI}domain/software/programming-language/name',
                   f'{BASE_URI}domain/software/programming-language/description')
        
@receiver(post_save, sender=Value)
def Dependency(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/software/dependency/id':
        add_basics(instance,
                   f'{BASE_URI}domain/software/dependency/name',
                   f'{BASE_URI}domain/software/dependency/description')
        
@receiver(post_save, sender=Value)
def CPU(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/hardware/cpu/id':
        add_basics(instance,
                   f'{BASE_URI}domain/hardware/cpu/name',
                   f'{BASE_URI}domain/hardware/cpu/description')
        
@receiver(post_save, sender=Value)
def Compiler(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/hardware/compiler/id':
        add_basics(instance,
                   f'{BASE_URI}domain/hardware/compiler/name',
                   f'{BASE_URI}domain/hardware/compiler/description')
        
@receiver(post_save, sender=Value)
def Location(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/instrument/location/id':
        add_basics(instance,
                   f'{BASE_URI}domain/instrument/location/name',
                   f'{BASE_URI}domain/instrument/location/description')
        
@receiver(post_save, sender=Value)
def AvailableSoftware(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/instrument/software/id':
        add_basics(instance,
                   f'{BASE_URI}domain/instrument/software/name',
                   f'{BASE_URI}domain/instrument/software/description')
        
@receiver(post_save, sender=Value)
def DataType(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/data-set/data-type/id':
        add_basics(instance,
                   f'{BASE_URI}domain/data-set/data-type/name',
                   f'{BASE_URI}domain/data-set/data-type/description')
        
@receiver(post_save, sender=Value)
def RepresentationFormat(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/data-set/representation-format/id':
        add_basics(instance,
                   f'{BASE_URI}domain/data-set/representation-format/name',
                   f'{BASE_URI}domain/data-set/representation-format/description')
        
@receiver(post_save, sender=Value)
def MainAlgorithm(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/main-algorithm/id':
        add_basics(instance,
                   f'{BASE_URI}domain/main-algorithm/name',
                   f'{BASE_URI}domain/main-algorithm/description')
        
@receiver(post_save, sender=Value)
def MainModel(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/main-model/id':
        add_basics(instance,
                   f'{BASE_URI}domain/main-model/name',
                   f'{BASE_URI}domain/main-model/description')
        
@receiver(post_save, sender=Value)
def ImplementingSoftware(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/main-algorithm/software/id':
        add_basics(instance,
                   f'{BASE_URI}domain/main-algorithm/software/name',
                   f'{BASE_URI}domain/main-algorithm/software/description')
        
@receiver(post_save, sender=Value)
def InputData(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    # Check if related Input Data Set concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Process Step Input ID"]["uri"]}':
        # Check if actual Input Data Set is chosen
        if instance.text:
            # Add Basic Information
            label, description, source = add_basics(instance,
                                                    f'{BASE_URI}{questions["Process Step Input Name"]["uri"]}',
                                                    f'{BASE_URI}{questions["Process Step Input Description"]["uri"]}')
            # If Data Set not defined by User
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Data Set"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Data Set ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "DS")
        
@receiver(post_save, sender=Value)
def OutputData(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    # Check if related Input Data Set concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Process Step Output ID"]["uri"]}':
        # Check if actual Input Data Set is chosen
        if instance.text:
            # Add Basic Information
            label, description, source = add_basics(instance,
                                                    f'{BASE_URI}{questions["Process Step Output Name"]["uri"]}',
                                                    f'{BASE_URI}{questions["Process Step Output Description"]["uri"]}')
            # If Data Set not defined by User
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Data Set"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Data Set ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "DS")
        
@receiver(post_save, sender=Value)
def Method(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    # Check if related Input Data Set concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Process Step Method ID"]["uri"]}':
        # Check if actual Input Data Set is chosen
        if instance.text:
            # Add Basic Information
            label, description, source = add_basics(instance,
                                                    f'{BASE_URI}{questions["Process Step Method Name"]["uri"]}',
                                                    f'{BASE_URI}{questions["Process Step Method Description"]["uri"]}')
            # If Data Set not defined by User
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Method"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Method ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "M")
        
@receiver(post_save, sender=Value)
def EnvironmentSoftware(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    # Check if related Input Data Set concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Process Step Environment-Software ID"]["uri"]}':
        # Check if actual Input Data Set is chosen
        if instance.text:
            # Add Basic Information
            label, description, source = add_basics(instance,
                                                    f'{BASE_URI}{questions["Process Step Environment-Software Name"]["uri"]}',
                                                    f'{BASE_URI}{questions["Process Step Environment-Software Description"]["uri"]}')
            # If Data Set not defined by User
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Software"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "S")
        
@receiver(post_save, sender=Value)
def EnvironmentInstrument(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    # Check if related Input Data Set concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Process Step Environment-Instrument ID"]["uri"]}':
        # Check if actual Input Data Set is chosen
        if instance.text:
            # Add Basic Information
            label, description, source = add_basics(instance,
                                                    f'{BASE_URI}{questions["Process Step Environment-Instrument Name"]["uri"]}',
                                                    f'{BASE_URI}{questions["Process Step Environment-Instrument Description"]["uri"]}')
            # If Data Set not defined by User
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Instrument"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Instrument ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "S")
        
@receiver(post_save, sender=Value)
def Discipline(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/process-step/discipline/id':
        add_basics(instance,
                   f'{BASE_URI}domain/process-step/discipline/name',
                   f'{BASE_URI}domain/process-step/discipline/description')
        
@receiver(post_save, sender=Value)
def SoftwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if (
        instance 
        and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog') 
        and instance.attribute.uri == f'{BASE_URI}domain/software/id'
        and instance.text and instance.text != 'not found'
        ):
        add_basics(instance, 
                   f'{BASE_URI}domain/software/name', 
                   f'{BASE_URI}domain/software/description')
        # Get source and ID of Item
        source, Id = instance.external_id.split(':')
        results = []
        if source == 'mardi':
            results = query_sparql(mardiProvider['Software'].format(wdt, wd, f"wd:{Id}", P19, P34, P35, P36, P16, P20), mardi_endpoint)
        elif source == 'wikidata':
            results = query_sparql(wikidataProvider['Software'].format(f"wd:{Id}"), wikidata_endpoint)
        if results:
            # Load Options
            options = get_data('data/options.json')
            # Add Reference of Software
            if results[0].get('doi', {}).get('value'):
                reference = f"doi:{results[0]['doi']['value']}"
            elif results[0].get('swmath', {}).get('value'):
                reference = f"sw:{results[0]['swmath']['value']}"
            else:
                reference = ''
            value_editor(instance.project, f'{BASE_URI}domain/software/reference', reference, None, None, None, instance.set_index, None)
            # Add Programming Languages of Software
            idx = 0
            if results[0].get(f'PL', {}).get('value'):
                for result in results[0]['PL']['value'].split(' / '):
                    ID, Label, Description = result.split(' | ')
                    value_editor(instance.project, f'{BASE_URI}domain/software/programming-language/id', f"{Label} ({Description}) [{source}]", f'{source}:{ID}', None, idx, instance.set_index, None)
                    idx += 1
            # Add Dependencies of Software
            idx = 0
            if results[0].get(f'DP', {}).get('value'):
                for result in results[0]['DP']['value'].split(' / '):
                    ID, Label, Description = result.split(' | ')
                    value_editor(instance.project, f'{BASE_URI}domain/software/dependency/id', f"{Label} ({Description}) [{source}]", f'{source}:{ID}', None, idx, instance.set_index, None)
                    idx += 1
            # Software Published?
            if results[0].get(f'published', {}).get('value'):
                value_editor(instance.project, f'{BASE_URI}domain/software/published', results[0]['published']['value'], None, options['YesText'], None, instance.set_index, None)
            # Software Documented?
            if results[0].get(f'documented', {}).get('value'):
                value_editor(instance.project, f'{BASE_URI}domain/software/documented', results[0]['documented']['value'], None, options['YesText'], None, instance.set_index, None)
    return

@receiver(post_save, sender=Value)
def HardwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/hardware/id':
        if instance.text and instance.text != 'not found':
            add_basics(instance, 
                       f'{BASE_URI}domain/hardware/name', 
                       f'{BASE_URI}domain/hardware/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            results = []
            if source == 'mardi':
                results = query_sparql(mardiProvider['Hardware'].format(wdt, wd, f"wd:{Id}", P26, P32, P31), mardi_endpoint)
            elif source == 'wikidata':
                results = query_sparql(wikidataProvider['Hardware'].format(f"wd:{Id}"), wikidata_endpoint)
            if results:
                # Add CPU of Hardware
                idx = 0
                if results[0].get(f'CPU', {}).get('value'):
                    for result in results[0]['CPU']['value'].split(' / '):
                        ID, Label, Description = result.split(' | ')
                        value_editor(instance.project, f'{BASE_URI}domain/hardware/cpu/id', f"{Label} ({Description}) [{source}]", f'{source}:{ID}', None, idx, instance.set_index, None)
                        idx += 1
                # Number of Nodes
                if results[0].get(f'nodes', {}).get('value'):
                    value_editor(instance.project, f'{BASE_URI}domain/hardware/nodes', results[0]['nodes']['value'], None, None, None, instance.set_index, None)
                # Number of Cores
                if results[0].get(f'cores', {}).get('value'):
                    value_editor(instance.project, f'{BASE_URI}domain/hardware/cores', results[0]['cores']['value'], None, None, None, instance.set_index, None)                
    return

@receiver(post_save, sender=Value)
def InstrumentInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/instrument/id':
        if instance.text and instance.text != 'not found':
            add_basics(instance, 
                       f'{BASE_URI}domain/instrument/name', 
                       f'{BASE_URI}domain/instrument/description')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            ### NEEDS ADDITIONS ###
    return

@receiver(post_save, sender=Value)
def DataSetInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/data-set/id':
        if instance.text and instance.text != 'not found':
            try:
                add_basics(instance, 
                           f'{BASE_URI}domain/data-set/name', 
                           f'{BASE_URI}domain/data-set/description')
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                results = []
                if source == 'mardi':
                    results = query_sparql(mardiProvider['DataSet'].format(wdt, wd, f"wd:{Id}", P37, P38, P39, P4, Q16, Q17, Q18, Q19, P16, P24, P40, Q20, Q21, P41, P6, P45, Q22, Q23), mardi_endpoint)
                elif source == 'wikidata':
                    results = query_sparql(wikidataProvider['DataSet'].format(f"wd:{Id}"), wikidata_endpoint)
                if results:
                    # Load Options
                    options = get_data('data/options.json')
                    # Data Set Size
                    if results[0].get('sizeValue', {}).get('value') and results[0].get('sizeUnit', {}).get('value'):
                        if results[0]['sizeUnit']['value'] in ['kilobyte','megabyte','gigabyte','terabyte']:
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/size', results[0]['sizeValue']['value'], None, options['kilobyte'], None, instance.set_index, None)
                    elif results[0].get('sizeRecord', {}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/data-set/size', results[0]['sizeRecord']['value'], None, options['items'], None, instance.set_index, None)
                    # Data Type
                    idx = 0
                    if results[0].get(f'DataType', {}).get('value'):
                        for result in results[0]['DataType']['value'].split(' / '):
                            ID, Label, Description = result.split(' | ')
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/data-type/id', f"{Label} ({Description}) [{source}]", f'{source}:{ID}', None, idx, instance.set_index, None)
                            idx += 1
                    # Representation Format
                    idx = 0
                    if results[0].get(f'RepresentationFormat', {}).get('value'):
                        for result in results[0]['RepresentationFormat']['value'].split(' / '):
                            ID, Label, Description = result.split(' | ')
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/representation-format/id', f"{Label} ({Description}) [{source}]", f'{source}:{ID}', None, idx, instance.set_index, None)
                            idx += 1
                    # File Format
                    if results[0].get('FileFormat', {}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/data-set/file-format', results[0]['FileFormat']['value'], None, None, None, instance.set_index, None)
                    # Binary or Text
                    if results[0].get('BinaryOrText', {}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/data-set/binary-or-text', None, None, options[results[0]['BinaryOrText']['value']], None, instance.set_index, None)
                    # Proprietary
                    if results[0].get('Proprietary', {}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/data-set/proprietary', None, None, options[results[0]['Proprietary']['value']], None, instance.set_index, None)
                    # Publishing
                    if results[0].get('Publishing', {}).get('value'):
                        if results[0].get('DOI', {}).get('value'):
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/to-publish', f"doi:{results[0]['DOI']['value']}", None, options[results[0]['Publishing']['value']], None, instance.set_index, None)
                        elif results[0].get('URL', {}).get('value'):
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/to-publish', f"url:{results[0]['URL']['value']}", None, options[results[0]['Publishing']['value']], None, instance.set_index, None)
                        else:
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/to-publish', None, None, options[results[0]['Publishing']['value']], None, instance.set_index, None)             
                    # Archiving
                    if results[0].get('Archiving', {}).get('value'):
                        if results[0].get('endTime', {}).get('value'):
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/to-archive', results[0]['endTime']['value'][:4], None, options[results[0]['Archiving']['value']], None, instance.set_index, None)
                        else:
                            value_editor(instance.project, f'{BASE_URI}domain/data-set/to-archive', None, None, options[results[0]['Archiving']['value']], None, instance.set_index, None)
            except:
                return

@receiver(post_save, sender=Value)
def ProcessStepInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Section
    questions = get_questionsWO()
    if instance and instance.attribute.uri == f'{BASE_URI}domain/process-step/id':
        if instance.text and instance.text != 'not found':
            add_basics(instance, 
                       f'{BASE_URI}{questions["Process Step Name"]["uri"]}',
                       f'{BASE_URI}{questions["Process Step Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            results = []
            if source == 'mardi':
                results = query_sparql(mardiProvider['ProcessStep'].format(wdt, wd, Id, P42, P43, P6, P44, P5, P25, P45, Q5, Q13), mardi_endpoint)
            elif source == 'wikidata':
                results = query_sparql(wikidataProvider['ProcessStep'].format(Id), wikidata_endpoint)

            if results:
                # Structure Results
                data = ProcessStep.from_query(results)
                
                # Add Relations between Input Data Set and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2IDS'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Input ID"]["uri"]}')
                
                # Add Relations between Output Data Set and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2ODS'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Output ID"]["uri"]}')
                
                # Add Relations between Method and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2M'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Method ID"]["uri"]}')
                
                # Add Relations between Software Platform and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2PLS'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Environment-Software ID"]["uri"]}')
                
                # Add Relations between Instrument Platform and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2PLI'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Environment-Instrument ID"]["uri"]}')
                
                # Add Relations between Fields and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2F'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Discipline ID"]["uri"]}')
                
                # Add Relations between Math Areas and Process Step to Questionnaire
                add_relations(project = instance.project, 
                              data = data, 
                              props = PROPS['PS2MA'], 
                              set_prefix = instance.set_index, 
                              relatant = f'{BASE_URI}{questions["Process Step Discipline ID"]["uri"]}')

    return

