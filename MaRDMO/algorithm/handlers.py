from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value

from .constants import PROPS, get_URI_PREFIX_MAP
from .sparql import queryHandlerAL
from .models import Benchmark, Software, Problem, Algorithm, Relatant

from ..config import BASE_URI, endpoint
from ..getters import get_mathalgodb, get_questions_algorithm, get_questions_publication
from ..helpers import extract_parts
from ..queries import query_sparql
from ..adders import add_basics, add_entities, add_new_entities, add_relations, add_references

@receiver(post_save, sender=Value)
def BenchmarkInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questions_algorithm() | get_questions_publication()
    # Check if Algorithm Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
        # Check if Benchmark ID concerned
        if instance.attribute.uri == f'{BASE_URI}{questions["Benchmark"]["ID"]["uri"]}':
            # Check if actual Benchmark chosen
            if instance.text and instance.text != 'not found':
                # Add Information to Questionnaire if not already present
                add_basics(project = instance.project,
                           text = instance.text,
                           questions = questions,
                           item_type = "Benchmark",
                           index = (0, instance.set_index)
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandlerAL['benchmarkInformation'].format(Id)
                results = query_sparql(query, endpoint[source]['sparql'])

                if results:
                    # Get Benchmark Data from Query
                    data = Benchmark.from_query(results)
                    # Add References to Questionnaire
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Benchmark"]["Reference"]["uri"]}',
                                   set_prefix = instance.set_index)
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def SoftwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questions_algorithm() | get_questions_publication()
    # Check if Algorithm Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
        # Check if Software ID concerned
        if instance.attribute.uri == f'{BASE_URI}{questions["Software"]["ID"]["uri"]}':
            # Check if actual Software chosen
            if instance.text and instance.text != 'not found':
                # Add Information to Questionnaire if not already present
                add_basics(project = instance.project,
                           text = instance.text,
                           questions = questions,
                           item_type = "Software",
                           index = (0, instance.set_index)
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                
                query = queryHandlerAL['softwareInformation'].format(Id)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathalgodb = get_mathalgodb()
                
                if results:
                    # Structure Results and load MathAlgoDB
                    data = Software.from_query(results)
                    # Add References to Questionnaire
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Software"]["Reference"]["uri"]}',
                                   set_prefix = instance.set_index)
                    # Add Benchmarks to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['S2B'], 
                                  mapping = mathalgodb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Software"]["BRelatant"]["uri"]}')
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def ProblemInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questions_algorithm() | get_questions_publication()
    # Check if Algorithm Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
        # Check if Algorithmic Problem ID concerned
        if instance.attribute.uri == f'{BASE_URI}{questions["Problem"]["ID"]["uri"]}':
            # Check if actual Algorithmic Problem chosen
            if instance.text and instance.text != 'not found':
                # Add Information to Questionnaire if not already present
                add_basics(project = instance.project,
                           text = instance.text,
                           questions = questions,
                           item_type = "Problem",
                           index = (0, instance.set_index)
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')    
                
                query = queryHandlerAL['softwareInformation'].format(Id)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathalgodb = get_mathalgodb()
                
                if results:
                    # Structure Data and load MathAlgoDB
                    data = Problem.from_query(results)
                    # Add Benchmarks to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['P2B'], 
                                  mapping = mathalgodb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Problem"]["BRelatant"]["uri"]}')
                    # Add Relations between Algorithmic Problems to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Problem'], 
                                  mapping = mathalgodb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Problem"]["IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Problem"]["IntraClassRelation"]["uri"]}')
    return

@receiver(post_save, sender=Value)
def AlgorithmInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questions_algorithm() | get_questions_publication()
    # Check if Algorithm Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
        # Check if Algorithm ID concerned
        if instance.attribute.uri == f'{BASE_URI}{questions["Algorithm"]["ID"]["uri"]}':
            # Check if actual Algorithm chosen
            if instance.text and instance.text != 'not found':
                # Load Questions of Algorithm Catalog
                # Add Information to Questionnaire if not already present
                add_basics(project = instance.project,
                           text = instance.text,
                           questions = questions,
                           item_type = "Algorithm",
                           index = (0, instance.set_index)
                           )
                # Get source and ID of Item
                source, Id = instance.external_id.split(':')
                
                query = queryHandlerAL['algorithmInformation'].format(Id)
                results = query_sparql(query, endpoint[source]['sparql'])
                mathalgodb = get_mathalgodb()
                
                if results:
                    # Structure Data and load MathAlgoDB
                    data = Algorithm.from_query(results)
                    # Add Algorithmic Problems to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['A2P'], 
                                  mapping = mathalgodb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Algorithm"]["PRelatant"]["uri"]}')
                    # Add Softwares to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['A2S'], 
                                  mapping = mathalgodb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Algorithm"]["SRelatant"]["uri"]}')
                    # Add Relations between Algorithms to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Algorithm'], 
                                  mapping = mathalgodb, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Algorithm"]["IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Algorithm"]["IntraClassRelation"]["uri"]}')
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def RelationHandler(sender, **kwargs):

    #Get Instance
    instance = kwargs.get("instance", None)

    # Check if Algorithm Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':

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
                    datas=datas,
                    source=source,
                    prefix=config["prefix"]
                )
            
            # Add items from user
            elif instance.external_id == 'not found':
                add_new_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    datas=datas,
                    prefix=config["prefix"]
                )

    return
