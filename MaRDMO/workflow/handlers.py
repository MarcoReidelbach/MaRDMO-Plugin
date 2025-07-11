from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value

from ..config import BASE_URI, endpoint
from ..getters import get_items, get_options, get_properties, get_questions_workflow
from ..helpers import extract_parts, value_editor
from ..queries import query_sparql
from ..adders import add_basics, add_entities, add_new_entities, add_references, add_relations

from .constants import PROPS, get_URI_PREFIX_MAP
from .models import Method, ProcessStep, Relatant, Software, Hardware, DataSet
from .sparql import queryHandler

@receiver(post_save, sender=Value)
def RelationHandler(sender, **kwargs):
    
    #Get Instance
    instance = kwargs.get("instance", None)
    
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

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

@receiver(post_save, sender=Value)
def SoftwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Catalog
        questions = get_questions_workflow()
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
                query = queryHandler[source]['software'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                
                if results:
                
                    # Structure Results and load options
                    data = Software.from_query(results)
                    options = get_options()
                    
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
                                  relatant = f'{BASE_URI}{questions["Software Programming Language"]["uri"]}')
                    
                    # Add Relations between Programming Language and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['S2DP'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Software Dependency"]["uri"]}')
                    
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
        questions = get_questions_workflow()
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
                query = queryHandler[source]['hardware'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                
                if results:

                    # Structure Results
                    data = Hardware.from_query(results)
                    
                    # Add Relations between CPU and Hardware to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['H2CPU'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Hardware CPU"]["uri"]}')
                    
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
        questions = get_questions_workflow()
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
        questions = get_questions_workflow()
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
                query = queryHandler[source]['data-set'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                
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
                                  relatant = f'{BASE_URI}{questions["Data Set Data Type"]["uri"]}')
                    
                    # Add Relations between Representation Format and Data Set to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['DS2RF'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Data Set Representation Format"]["uri"]}')
                        
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
        questions = get_questions_workflow()
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
                query = queryHandler[source]['method'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                
                if results:
                    # Structure Results
                    data = Method.from_query(results)

                    # Add Relations between Software and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['M2S'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Method Software"]["uri"]}')

                    # Add Relations between Instrument and Method to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['M2I'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Method Instrument"]["uri"]}')
                    
                
    return

@receiver(post_save, sender=Value)
def ProcessStepInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Workflow Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
        # Get Questions of Workflow Section
        questions = get_questions_workflow()
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
                query = queryHandler[source]['step'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                
                if results:
                    # Structure Results
                    data = ProcessStep.from_query(results)

                    # Add Relations between Input Data Set and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2IDS'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Input"]["uri"]}')

                    # Add Relations between Output Data Set and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2ODS'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Output"]["uri"]}')

                    # Add Relations between Method and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2M'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Method"]["uri"]}')

                    # Add Relations between Software Platform and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2PLS'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Environment-Software"]["uri"]}')

                    # Add Relations between Instrument Platform and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2PLI'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Environment-Instrument"]["uri"]}')

                    # Add Relations between Fields and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2F'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Discipline"]["uri"]}')

                    # Add Relations between Math Areas and Process Step to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['PS2MA'], 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Process Step Discipline"]["uri"]}')
    return

