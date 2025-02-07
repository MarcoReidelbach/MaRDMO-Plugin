from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value

from .constants import PROPS
from .sparql import queryHandlerAL
from .models import Benchmark, Software, Problem, Algorithm, Relatant

from ..config import BASE_URI
from ..utils import add_basics, add_entities, add_relations, add_references, extract_parts, get_data, get_questionsAL, query_sparql, value_editor

@receiver(post_save, sender=Value)
def BenchmarkInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if Benchmark ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Benchmark ID"]["uri"]}':
        # Check if actual Benchmark chosen
        if instance.text and instance.text != 'not found':
            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}{questions["Benchmark Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Benchmark Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathalgodb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandlerAL['benchmarkInformation'].format(Id))
                if results:
                    # Get Benchmark Data from Query
                    data = Benchmark.from_query(results)
                    
                    # Add References to Questionnaire
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Benchmark Reference"]["uri"]}',
                                   set_prefix = instance.set_index)
                    
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def SoftwareInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if Software ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Software ID"]["uri"]}':
        # Check if actual Software chosen
        if instance.text and instance.text != 'not found':
            # Load Options
            options = get_data('data/options.json')
            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}{questions["Software Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Software Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathalgodb':
                # If Item from MathAlgoDB get further Information
                results = query_sparql(queryHandlerAL['softwareInformation'].format(Id))
                if results:
                    # Structure Results and load MathAlgoDB
                    data = Software.from_query(results)
                    mathalgodb = get_data('algorithm/data/mapping.json')
                    
                    # Add References to Questionnaire
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Software Reference"]["uri"]}',
                                   set_prefix = instance.set_index)
                    
                    # Add Benchmarks to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['S2B'], 
                                  mapping = mathalgodb, 
                                  source = source, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Software BRelatant"]["uri"]}')
                    
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def ProblemInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if Algorithmic Problem ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Problem ID"]["uri"]}':
        # Check if actual Algorithmic Problem chosen
        if instance.text and instance.text != 'not found':
            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}{questions["Problem Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Problem Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')    
            if source== 'mathalgodb':
                # If Item from MathAlgoDB get further Information
                results = query_sparql(queryHandlerAL['problemInformation'].format(Id))
                if results:
                    # Structure Data and load MathAlgoDB
                    data = Problem.from_query(results)
                    mathalgodb = get_data('algorithm/data/mapping.json')
    
                    # Add Benchmarks to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['P2B'], 
                                  mapping = mathalgodb, 
                                  source = source, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Problem BRelatant"]["uri"]}')
                    
                    # Add Relations between Algorithmic Problems to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Problem'], 
                                  mapping = mathalgodb, 
                                  source = source, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Problem IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Problem IntraClassRelation"]["uri"]}')
    return

@receiver(post_save, sender=Value)
def AlgorithmInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if Algorithm ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Algorithm ID"]["uri"]}':
        # Check if actual Algorithm chosen
        if instance.text and instance.text != 'not found':
            # Load Questions of Algorithm Catalog
            questions = get_data('algorithm/data/questions.json')
            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}{questions["Algorithm Name"]["uri"]}', 
                       f'{BASE_URI}{questions["Algorithm Description"]["uri"]}')
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathalgodb':
                # If Item from MathAlgoDB get further Information
                results = query_sparql(queryHandlerAL['algorithmInformation'].format(Id))
                if results:
                    # Structure Data and load MathAlgoDB
                    data = Algorithm.from_query(results)
                    mathalgodb = get_data('algorithm/data/mapping.json')
    
                    # Add Algorithmic Problems to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['A2P'], 
                                  mapping = mathalgodb, 
                                  source = source, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Algorithm PRelatant"]["uri"]}')
    
                    # Add Softwares to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['A2S'], 
                                  mapping = mathalgodb, 
                                  source = source, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Algorithm SRelatant"]["uri"]}')
    
                    # Add Relations between Algorithms to Questionnaire
                    add_relations(project = instance.project, 
                                  data = data, 
                                  props = PROPS['Algorithm'], 
                                  mapping = mathalgodb, 
                                  source = source, 
                                  set_prefix = instance.set_index, 
                                  relatant = f'{BASE_URI}{questions["Algorithm IntraClassElement"]["uri"]}', 
                                  relation = f'{BASE_URI}{questions["Algorithm IntraClassRelation"]["uri"]}')
                    
                    # Add Publications to Questionnaire
                    add_entities(project = instance.project, 
                                 question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                                 question_id = f'{BASE_URI}{questions["Publication ID"]["uri"]}',
                                 datas = data.publications, 
                                 source = source,
                                 prefix = 'P')
    return

@receiver(post_save, sender=Value)
def BenchmarkProblemRelation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if related Benchmark is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Problem BRelatant"]["uri"]}':
        # Check if actual Benchmark chosen
        if instance.text:
            mathalgodb = get_data('algorithm/data/mapping.json')
            label, description, source =  extract_parts(instance.text)
            # Add Benchmark Relation to questionnaire
            value_editor(project = instance.project, 
                         uri = f'{BASE_URI}{questions["Problem P2B"]["uri"]}', 
                         text = mathalgodb['instantiates'],
                         collection_index = instance.collection_index, 
                         set_index = 0, 
                         set_prefix = instance.set_prefix)
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Benchmark"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Benchmark ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "B")
                
@receiver(post_save, sender=Value)
def BenchmarkSoftwareRelation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if related Benchmark is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Software BRelatant"]["uri"]}':
        # Check if actual Benchmark chosen
        if instance.text:
            mathalgodb = get_data('algorithm/data/mapping.json')
            label, description, source =  extract_parts(instance.text)
            # Add Benchmark Relation to questionnaire
            value_editor(project = instance.project, 
                         uri = f'{BASE_URI}{questions["Software S2B"]["uri"]}', 
                         text = mathalgodb['tests'], 
                         collection_index = instance.collection_index, 
                         set_index = 0, 
                         set_prefix = instance.set_prefix)
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Benchmark"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Benchmark ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "B")
                
@receiver(post_save, sender=Value)
def AlgorithmProblemRelation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if related Problem is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Algorithm PRelatant"]["uri"]}':
        # Check if actual Problem chosen
        if instance.text:
            mathalgodb = get_data('algorithm/data/mapping.json')
            label, description, source =  extract_parts(instance.text)
            # Add Problem Relation to questionnaire
            value_editor(project = instance.project, 
                         uri = f'{BASE_URI}{questions["Algorithm A2P"]["uri"]}', 
                         text = mathalgodb['solves'], 
                         collection_index = instance.collection_index, 
                         set_index = 0, 
                         set_prefix = instance.set_prefix)
            if source != 'user':
                add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Problem"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Problem ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "AP")
                
@receiver(post_save, sender=Value)
def AlgorithmSoftwareRelation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if related Software is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Algorithm SRelatant"]["uri"]}':
            # Check if actual Benchmark chosen
            if instance.text:
                mathalgodb = get_data('algorithm/data/mapping.json')
                label, description, source =  extract_parts(instance.text)
                # Add Problem Relation to questionnaire
                value_editor(project = instance.project, 
                             uri = f'{BASE_URI}{questions["Algorithm A2S"]["uri"]}', 
                             text = mathalgodb['implementedBy'], 
                             collection_index = instance.collection_index, 
                             set_index = 0, 
                             set_prefix = instance.set_prefix)
                if source != 'user':
                    add_entities(project = instance.project, 
                             question_set = f'{BASE_URI}{questions["Software"]["uri"]}', 
                             question_id = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                             datas = [Relatant.from_relation(instance.external_id, label, description)], 
                             source = source, 
                             prefix = "S")
                    

                
                
                