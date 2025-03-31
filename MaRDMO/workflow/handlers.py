from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value

from ..config import BASE_URI, endpoint
from ..utils import add_basics, add_entities, add_references, add_relations, get_data, get_questionsWO, value_editor, query_sparql

from .sparql import queryInfo
from .models import Method, ProcessStep, Relatant, Software, Hardware, DataSet
from .constants import PROPS

@receiver(post_save, sender=Value)
def BasicInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Software Programming Language
        if instance.attribute.uri == f'{BASE_URI}{questions["Software Programming Language ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Software Programming Language Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Software Programming Language Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Software Dependency
        elif instance.attribute.uri == f'{BASE_URI}{questions["Software Dependency ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Software Dependency Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Software Dependency Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Hardware CPU
        elif instance.attribute.uri == f'{BASE_URI}{questions["Hardware CPU ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Hardware CPU Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Hardware CPU Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Instrument Location
        elif instance.attribute.uri == f'{BASE_URI}{questions["Hardware Compiler ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Hardware Compiler Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Hardware Compiler Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Instrument Location
        elif instance.attribute.uri == f'{BASE_URI}{questions["Instrument Location ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Instrument Location Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Instrument Location Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Data Set Data Type
        elif instance.attribute.uri == f'{BASE_URI}{questions["Data Set Data Type ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Data Set Data Type Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Data Set Data Type Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Data Set Representation Format
        elif instance.attribute.uri == f'{BASE_URI}{questions["Data Set Representation Format ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Data Set Representation Format Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Data Set Representation Format Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
        # Mathematical Model
        elif instance.attribute.uri == f'{BASE_URI}{questions["Model ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Model Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Model Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       ) 
        # Discipline
        elif instance.attribute.uri == f'{BASE_URI}{questions["Process Step Discipline ID"]["uri"]}':
            add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Process Step Discipline Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Process Step Discipline Description"]["uri"]}',
                       collection_index = instance.collection_index,
                       set_index = instance.set_index,
                       set_prefix = instance.set_prefix
                       )
    return
        
@receiver(post_save, sender=Value)
def BasicInformationAndEntryAddition(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Workflow Catalog
    questions = get_questionsWO()
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Input Data Set
        if instance.attribute.uri == f'{BASE_URI}{questions["Process Step Input ID"]["uri"]}':
            # Check if actual Input Data Set is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Process Step Input Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Process Step Input Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Data Set"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Data Set ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "DS")
        # Output Data Set
        elif instance.attribute.uri == f'{BASE_URI}{questions["Process Step Output ID"]["uri"]}':
            # Check if actual Output Data Set is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Process Step Output Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Process Step Output Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Data Set"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Data Set ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "DS")
        # Method
        elif instance.attribute.uri == f'{BASE_URI}{questions["Process Step Method ID"]["uri"]}':
            # Check if actual Method is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Process Step Method Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Process Step Method Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Method"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Method ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "M")
        # Environment Software
        elif instance.attribute.uri == f'{BASE_URI}{questions["Process Step Environment-Software ID"]["uri"]}':
            # Check if actual Environment Software is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Process Step Environment-Software Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Process Step Environment-Software Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Software"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "S")
        # Environemnt Instrument
        elif instance.attribute.uri == f'{BASE_URI}{questions["Process Step Environment-Instrument ID"]["uri"]}':
            # Check if actual Input Data Set is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Process Step Environment-Instrument Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Process Step Environment-Instrument Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Instrument"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Instrument ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "I")
        # Implementing Software
        elif instance.attribute.uri == f'{BASE_URI}{questions["Method Software ID"]["uri"]}':
            # Check if actual Software is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Method Software Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Method Software Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Software"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "S")
        # Implementing Instrument
        elif instance.attribute.uri == f'{BASE_URI}{questions["Method Instrument ID"]["uri"]}':
            # Check if actual Instrument is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Method Instrument Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Method Instrument Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Instrument"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Instrument ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "I")
        # Instrument Software
        elif instance.attribute.uri == f'{BASE_URI}{questions["Instrument Software ID"]["uri"]}':
            # Check if actual Software is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Instrument Software Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Instrument Software Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Software"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "S")
        # Hardware Software
        elif instance.attribute.uri == f'{BASE_URI}{questions["Hardware Software ID"]["uri"]}':
            # Check if actual Software is chosen
            if instance.text:
                # Add Basic Information
                label, description, source = add_basics(project = instance.project,
                                                        text = instance.text,
                                                        url_name = f'{BASE_URI}{questions["Hardware Software Name"]["uri"]}',
                                                        url_description = f'{BASE_URI}{questions["Hardware Software Description"]["uri"]}',
                                                        collection_index = instance.collection_index,
                                                        set_index = instance.set_index,
                                                        set_prefix = instance.set_prefix
                                                        )
                # If Data Set not defined by User
                if source != 'user':
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Software"]["uri"]}', 
                                 question_id = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                                 datas = [Relatant.from_relation(instance.external_id, label, description)], 
                                 source = source, 
                                 prefix = "S")
        
        
    return

@receiver(post_save, sender=Value)
def SoftwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Catalog
        questions = get_questionsWO()
        # Check if Software ID is concerned
        if instance.attribute.uri == f'{BASE_URI}{questions["Software ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                
                # Add Basic Information
                add_basics(project = instance.project,
                               text = instance.text,
                               url_name = f'{BASE_URI}{questions["Software Name"]["uri"]}',
                               url_description = f'{BASE_URI}{questions["Software Description"]["uri"]}',
                               set_index = 0,
                               set_prefix = instance.set_index
                               )
                
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # Query source for further Information
                results = query_sparql(queryInfo[source]['software'].format(Id), endpoint[source]['sparql'])
                
                if results:
                
                    # Structure Results and load options
                    data = Software.from_query(results)
                    options = get_data('data/options.json')
                    
                    # Add References to Questionnaire
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Software Reference"]["uri"]}',
                                   set_prefix = instance.set_index)
                    
                    # Add Relations between Programming Language and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['S2PL'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Software Programming Language ID"]["uri"]}')
                    
                    # Add Relations between Programming Language and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['S2DP'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Software Dependency ID"]["uri"]}')
                    
                    # Software Source Code Published?
                    if data.sourceCodeRepository:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Software Published"]["uri"]}', 
                                     text = data.sourceCodeRepository, 
                                     option = options['YesText'], 
                                     set_prefix = instance.set_index)
                        
                    # Software User Manual Documented?
                    if data.userManualURL: 
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Software Documented"]["uri"]}', 
                                     text = data.userManualURL,
                                     option = options['YesText'],
                                     set_prefix = instance.set_index)
    return

@receiver(post_save, sender=Value)
def HardwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Section
        questions = get_questionsWO()
        if instance.attribute.uri == f'{BASE_URI}{questions["Hardware ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add Basic Information
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Hardware Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Hardware Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # Query source for further Information
                results = query_sparql(queryInfo[source]['hardware'].format(Id), endpoint[source]['sparql'])

                if results:

                    # Structure Results
                    data = Hardware.from_query(results)
                    
                    # Add Relations between CPU and Hardware to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['H2CPU'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Hardware CPU ID"]["uri"]}')
                    
                    # Number of Nodes
                    if data.nodes:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Hardware Nodes"]["uri"]}', 
                                     text = data.nodes, 
                                     set_prefix = instance.set_index)
                    
                    # Number of Cores
                    if data.cores:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Hardware Cores"]["uri"]}', 
                                     text = data.cores, 
                                     set_prefix = instance.set_index)                
    return

@receiver(post_save, sender=Value)
def InstrumentInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Section
        questions = get_questionsWO()
        if instance.attribute.uri == f'{BASE_URI}{questions["Instrument ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add Basic Information
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Instrument Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Instrument Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
    
    return

@receiver(post_save, sender=Value)
def DataSetInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Section
        questions = get_questionsWO()
        if instance.attribute.uri == f'{BASE_URI}{questions["Data Set ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add Basic Information
                add_basics(project = instance.project,
                       text = instance.text,
                       url_name = f'{BASE_URI}{questions["Data Set Name"]["uri"]}',
                       url_description = f'{BASE_URI}{questions["Data Set Description"]["uri"]}',
                       set_index = 0,
                       set_prefix = instance.set_index
                       )
                
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # Query source for further Information
                results = query_sparql(queryInfo[source]['data-set'].format(Id), endpoint[source]['sparql'])

                if results:
                    
                    # Structure Results and load Pptions
                    data = DataSet.from_query(results)
                    
                    # Data Set Size
                    if data.size: 
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Data Set Size"]["uri"]}', 
                                     text = data.size[1],
                                     option = data.size[0],
                                     set_prefix = instance.set_index)
                        
                    # Add Relations between Data Type and Data Set to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['DS2DT'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Data Set Data Type ID"]["uri"]}')
                    
                    # Add Relations between Representation Format and Data Set to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['DS2RF'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Data Set Representation Format ID"]["uri"]}')
                        
                    # File Format
                    if data.fileFormat:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Data Set File Format"]["uri"]}', 
                                     text = data.fileFormat, 
                                     set_prefix = instance.set_index)
                    
                    # Binary or Text
                    if data.binaryOrText:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Data Set Binary or Text"]["uri"]}', 
                                     option = data.binaryOrText, 
                                     set_prefix = instance.set_index)
                    
                    # Proprietary
                    if data.proprietary:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Data Set Proprietary"]["uri"]}', 
                                     option = data.proprietary, 
                                     set_prefix = instance.set_index)
                        
                    # References To Publish
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Data Set To Publish"]["uri"]}',
                                   set_prefix = instance.set_index)
                    
                    # Archiving
                    if data.toArchive:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Data Set To Archive"]["uri"]}', 
                                     text = data.toArchive[1],
                                     option = data.toArchive[0], 
                                     set_prefix = instance.set_index)
                    
    return

@receiver(post_save, sender=Value)
def MethodInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Section
        questions = get_questionsWO()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Method ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                
                # Add Basic Information to Questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Method Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Method Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')

                # Query source for further Information
                results = query_sparql(queryInfo[source]['method'].format(Id), endpoint[source]['sparql'])

                if results:
                    # Structure Results
                    data = Method.from_query(results)

                    # Add Relations between Software and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['M2S'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Method Software ID"]["uri"]}')

                    # Add Relations between Instrument and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['M2I'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Method Instrument ID"]["uri"]}')
                    
                
    return

@receiver(post_save, sender=Value)
def ProcessStepInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Section
        questions = get_questionsWO()
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Process Step ID"]["uri"]}':
            if instance.text and instance.text != 'not found':
                
                # Add Basic Information to Questionnaire
                add_basics(project = instance.project,
                           text = instance.text,
                           url_name = f'{BASE_URI}{questions["Process Step Name"]["uri"]}',
                           url_description = f'{BASE_URI}{questions["Process Step Description"]["uri"]}',
                           set_index = 0,
                           set_prefix = instance.set_index
                           )
                
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                
                # Query source for further Information
                results = query_sparql(queryInfo[source]['step'].format(Id), endpoint[source]['sparql'])
                
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

