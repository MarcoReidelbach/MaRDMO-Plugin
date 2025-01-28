from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option
from rdmo.domain.models import Attribute

from .sparql import queryHandlerAL

from ..config import BASE_URI
from ..workflow.utils import add_entity
from ..utils import extract_parts, get_data, information_exists, query_sparql, value_editor

from ..model.utils import add_basics, get_id

@receiver(post_save, sender=Value)
def BenchmarkInformation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    # Check if Benchmark ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}domain/benchmark/id':

        # Check if actual Benchmark chosen
        if instance.text and instance.text != 'not found':

            # Check if Information already in Questionnaire
            if information_exists(instance.project, 'benchmark', instance.set_index):
                return

            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}domain/benchmark/name', 
                       f'{BASE_URI}domain/benchmark/description')
            
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathalgodb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandlerAL['benchmarkInformation'].format(f":{Id}"))
                if results:
                    # Add Identifier to Questionnaire
                    if results[0].get('reference', {}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/benchmark/reference', results[0]['reference']['value'], None, None, None, 0, instance.set_index)
    
                    # Add Publications to Questionnaire
                    add_entity(instance, results,
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P', 'mathalgodb')
    return

@receiver(post_save, sender=Value)
def SoftwareInformation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    # Check if Benchmark ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}domain/software/id':

        # Check if actual Benchmark chosen
        if instance.text and instance.text != 'not found':

            # Check if Information already in Questionnaire
            if information_exists(instance.project, 'software', instance.set_index):
                return

            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}domain/software/name', 
                       f'{BASE_URI}domain/software/description')
            
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathalgodb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandlerAL['softwareInformation'].format(f":{Id}"))
                if results:
                    # Add Identifier to Questionnaire
                    if results[0].get('reference', {}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/software/reference', results[0]['reference']['value'], None, None, None, 0, instance.set_index)
    
                    # Add Benchmarks to Questionnaire
                    if results[0].get('benchmark', {}).get('value'):
                        benchmarks = results[0]['benchmark']['value'].split(' / ')
                        for idx, benchmark in enumerate(benchmarks):
                            Id, Name, Description = benchmark.split(' | ') 
                            value_editor(instance.project, f'{BASE_URI}domain/software/benchmark-relatant', f"{Name} ({Description}) [mathalgodb]", f"mathalgodb:{Id}", None, idx, 0, instance.set_index)

                    # Add Publications to Questionnaire
                    add_entity(instance, results,
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P', 'mathalgodb')
    return

@receiver(post_save, sender=Value)
def AlgorithmicProblemInformation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    # Check if Benchmark ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}domain/algorithmic-problem/id':

        # Check if actual Benchmark chosen
        if instance.text and instance.text != 'not found':

            # Check if Information already in Questionnaire
            if information_exists(instance.project, 'algorithmic-problem', instance.set_index):
                return

            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}domain/algorithmic-problem/name', 
                       f'{BASE_URI}domain/algorithmic-problem/description')
            
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            
            if source== 'mathalgodb':

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandlerAL['algorithmicProblemInformation'].format(f":{Id}"))
                
                if results:

                    # Load MathAlgoDB
                    mathalgodb = get_data('algorithm/data/mapping.json')
                    
                    # Add Benchmarks to Questionnaire
                    if results[0].get('benchmark', {}).get('value'):
                        benchmarks = results[0]['benchmark']['value'].split(' / ')
                        for idx, benchmark in enumerate(benchmarks):
                            Id, Name, Description = benchmark.split(' | ') 
                            value_editor(instance.project, f'{BASE_URI}domain/algorithmic-problem/benchmark-relatant', f"{Name} ({Description}) [mathalgodb]", f"mathalgodb:{Id}", None, idx, 0, instance.set_index)

                    # Add related Problems to Questionnaire
                    props = ['specializes', 'specializedBy']
                    idx = 0
                    for prop in props:
                        if results[0].get(prop, {}).get('value'):
                            problems = results[0][prop]['value'].split(' / ')
                            for problem in problems:
                                Id, Name, Description = problem.split(' | ') 
                                value_editor(instance.project, f'{BASE_URI}domain/algorithmic-problem/algorithmic-problem-relation', None, None, Option.objects.get(uri=mathalgodb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/algorithmic-problem/algorithmic-problem-relatant', f"{Name} ({Description}) [mathalgodb]", f"mathalgodb:{Id}", None, None, idx, instance.set_index)
                                idx += 1

                    # Add Publications to Questionnaire
                    add_entity(instance, results,
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P', 'mathalgodb')
    return

@receiver(post_save, sender=Value)
def AlgorithmInformation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    # Check if Benchmark ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}domain/algorithm/id':

        # Check if actual Benchmark chosen
        if instance.text and instance.text != 'not found':

            # Check if Information already in Questionnaire
            if information_exists(instance.project, 'algorithm', instance.set_index):
                return

            # Add Information to Questionnaire if not already present
            add_basics(instance, 
                       f'{BASE_URI}domain/algorithm/name', 
                       f'{BASE_URI}domain/algorithm/description')
            
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            
            if source== 'mathalgodb':

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandlerAL['algorithmInformation'].format(f":{Id}"))

                if results:

                    # Load MathAlgoDB
                    mathalgodb = get_data('algorithm/data/mapping.json')
                    
                    # Add Problem to Questionnaire
                    if results[0].get('problem', {}).get('value'):
                        problems = results[0]['problem']['value'].split(' / ')
                        for idx, problem in enumerate(problems):
                            Id, Name, Description = problem.split(' | ') 
                            value_editor(instance.project, f'{BASE_URI}domain/algorithm/algorithmic-problem-relatant', f"{Name} ({Description}) [mathalgodb]", f"mathalgodb:{Id}", None, idx, 0, instance.set_index)

                    # Add Software to Questionnaire
                    if results[0].get('software', {}).get('value'):
                        softwares = results[0]['software']['value'].split(' / ')
                        for idx, software in enumerate(softwares):
                            Id, Name, Description = software.split(' | ') 
                            value_editor(instance.project, f'{BASE_URI}domain/algorithm/software-relatant', f"{Name} ({Description}) [mathalgodb]", f"mathalgodb:{Id}", None, idx, 0, instance.set_index)

                    # Add related Algorithms to Questionnaire
                    props = ['hasComponent', 'componentOf', 'hasSubclass', 'subclassOf', 'relatedTo']
                    idx = 0
                    for prop in props:
                        if results[0].get(prop, {}).get('value'):
                            algorithms = results[0][prop]['value'].split(' / ')
                            for algorithm in algorithms:
                                Id, Name, Description = algorithm.split(' | ') 
                                value_editor(instance.project, f'{BASE_URI}domain/algorithm/algorithm-relation', None, None, Option.objects.get(uri=mathalgodb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/algorithm/algorithm-relatant', f"{Name} ({Description}) [mathalgodb]", f"mathalgodb:{Id}", None, None, idx, instance.set_index)
                                idx += 1

                    # Add Publications to Questionnaire
                    add_entity(instance, results,
                               f'{BASE_URI}domain/publication', 
                               f'{BASE_URI}domain/publication/id', 
                               'publication', 'P', 'mathalgodb')
    return

                


@receiver(post_save, sender=Value)
def BenchmarkProblemRelation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    if instance:

        # Check if Benchmark concerned
        if instance.attribute.uri == f'{BASE_URI}domain/algorithmic-problem/benchmark-relatant':

            # Check if actual Benchmark chosen
            if instance.text:

                mathalgodb = get_data('algorithm/data/mapping.json')

                label, description, source =  extract_parts(instance.text)

                # Add Benchmark Relation to questionnaire
                value_editor(instance.project, f'{BASE_URI}domain/algorithmic-problem/benchmark-relation', mathalgodb['instantiates'], None, None, instance.collection_index, 0, instance.set_prefix)

                if source != 'user':

                    ID = instance.external_id

                    # Get (set) ids of exisitng benchmark in questionnaire
                    set_ids = get_id(instance, f'{BASE_URI}domain/benchmark', ['set_index'])
                    value_ids = get_id(instance, f'{BASE_URI}domain/benchmark/id', ['external_id'])

                    # Add Benchmark entry to questionnaire
                    idx = max(set_ids, default = -1) + 1
                    if ID not in value_ids:
                        # Set up Page
                        value_editor(instance.project, f'{BASE_URI}domain/benchmark', f"B{idx}", None, None, None, idx)
                        # Add ID Values
                        value_editor(instance.project, f'{BASE_URI}domain/benchmark/id', f'{label} ({description}) [{source}]', f"{ID}", None, None, idx)
                        idx += 1
                        value_ids.append(ID)

@receiver(post_save, sender=Value)
def BenchmarkSoftwareRelation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    if instance:

        # Check if Benchmark concerned
        if instance.attribute.uri == f'{BASE_URI}domain/software/benchmark-relatant':

            # Check if actual Benchmark chosen
            if instance.text:

                mathalgodb = get_data('algorithm/data/mapping.json')

                label, description, source =  extract_parts(instance.text)

                # Add Benchmark Relation to questionnaire
                value_editor(instance.project, f'{BASE_URI}domain/software/benchmark-relation', mathalgodb['tests'], None, None, instance.collection_index, 0, instance.set_prefix)

                if source != 'user':

                    ID = instance.external_id

                    # Get (set) ids of exisitng benchmark in questionnaire
                    set_ids = get_id(instance, f'{BASE_URI}domain/benchmark', ['set_index'])
                    value_ids = get_id(instance, f'{BASE_URI}domain/benchmark/id', ['external_id'])

                    # Add Benchmark entry to questionnaire
                    idx = max(set_ids, default = -1) + 1
                    if ID not in value_ids:
                        # Set up Page
                        value_editor(instance.project, f'{BASE_URI}domain/benchmark', f"B{idx}", None, None, None, idx)
                        # Add ID Values
                        value_editor(instance.project, f'{BASE_URI}domain/benchmark/id', f'{label} ({description}) [{source}]', f"{ID}", None, None, idx)
                        idx += 1
                        value_ids.append(ID)

@receiver(post_save, sender=Value)
def AlgorithmProblemRelation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    if instance:

        # Check if Benchmark concerned
        if instance.attribute.uri == f'{BASE_URI}domain/algorithm/algorithmic-problem-relatant':

            # Check if actual Benchmark chosen
            if instance.text:

                mathalgodb = get_data('algorithm/data/mapping.json')

                label, description, source =  extract_parts(instance.text)

                # Add Problem Relation to questionnaire
                value_editor(instance.project, f'{BASE_URI}domain/algorithm/algorithmic-problem-relation', mathalgodb['solves'], None, None, instance.collection_index, 0, instance.set_prefix)

                if source != 'user':

                    ID = instance.external_id

                    # Get (set) ids of exisitng problems in questionnaire
                    set_ids = get_id(instance, f'{BASE_URI}domain/algorithmic-problem', ['set_index'])
                    value_ids = get_id(instance, f'{BASE_URI}domain/algorithmic-problem/id', ['external_id'])

                    # Add Problem entry to questionnaire
                    idx = max(set_ids, default = -1) + 1
                    if ID not in value_ids:
                        # Set up Page
                        value_editor(instance.project, f'{BASE_URI}domain/algorithmic-problem', f"P{idx}", None, None, None, idx)
                        # Add ID Values
                        value_editor(instance.project, f'{BASE_URI}domain/algorithmic-problem/id', f'{label} ({description}) [{source}]', f"{ID}", None, None, idx)
                        idx += 1
                        value_ids.append(ID)

@receiver(post_save, sender=Value)
def AlgorithmSoftwareRelation(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    if instance:

        # Check if Benchmark concerned
        if instance.attribute.uri == f'{BASE_URI}domain/algorithm/software-relatant':

            # Check if actual Benchmark chosen
            if instance.text:

                mathalgodb = get_data('algorithm/data/mapping.json')

                label, description, source =  extract_parts(instance.text)

                # Add Problem Relation to questionnaire
                value_editor(instance.project, f'{BASE_URI}domain/algorithm/software-relation', mathalgodb['implementedBy'], None, None, instance.collection_index, 0, instance.set_prefix)

                if source != 'user':

                    ID = instance.external_id

                    # Get (set) ids of exisitng software in questionnaire
                    set_ids = get_id(instance, f'{BASE_URI}domain/software', ['set_index'])
                    value_ids = get_id(instance, f'{BASE_URI}domain/software/id', ['external_id'])

                    # Add Software entry to questionnaire
                    idx = max(set_ids, default = -1) + 1
                    if ID not in value_ids:
                        # Set up Page
                        value_editor(instance.project, f'{BASE_URI}domain/software', f"P{idx}", None, None, None, idx)
                        # Add ID Values
                        value_editor(instance.project, f'{BASE_URI}domain/software/id', f'{label} ({description}) [{source}]', f"{ID}", None, None, idx)
                        idx += 1
                        value_ids.append(ID)



                
                
                