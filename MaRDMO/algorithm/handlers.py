from django.dispatch import receiver
from django.db.models.signals import post_save
from django.apps import apps

from rdmo.projects.models import Value
from rdmo.options.models import Option

from .sparql import queryHandlerAL
from .models import Benchmark, Software, AlgorithmicProblem, Algorithm

from ..config import BASE_URI
from ..utils import extract_parts, get_id, get_data, get_questionsAL, query_sparql, value_editor

from ..model.utils import add_basics
from ..publication.utils import add_publication

@receiver(post_save, sender=Value)
def BenchmarkInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Algorithm Catalog
    questions = get_questionsAL()
    # Check if Benchmark ID concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Benchmark ID"]["uri"]}':
        # Check if actual Benchmark chosen
        if instance.text and instance.text != 'not found':
            # Load Options
            options = get_data('data/options.json')
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
                    # Add Identifier to Questionnaire
                    for reference in data.reference:
                        reference_prefix, reference_id = reference.split(':')
                        value_editor(project = instance.project, 
                                     uri  = f'{BASE_URI}{questions["Benchmark Reference"]["uri"]}', 
                                     text = reference_id,
                                     option = Option.objects.get(uri=options['MORWIKI']) if reference_prefix == 'morwiki' else Option.objects.get(uri=options['DOI']) if reference_prefix == 'doi' else None,
                                     collection_index = 0 if reference_prefix == 'morwiki' else 1 if reference_prefix == 'doi' else None,
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Publications to Questionnaire
                    add_publication(instance, data.publications, source)
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
                    # Structure Results
                    data = Software.from_query(results)
                    # Add Identifier to Questionnaire
                    for reference in data.reference:
                        reference_prefix, reference_id = reference.split(':')
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Software Reference"]["uri"]}', 
                                     text = reference_id, 
                                     option = Option.objects.get(uri=options['SWMATH']) if reference_prefix == 'swmath' else Option.objects.get(uri=options['DOI']) if reference_prefix == 'doi' else None,
                                     collection_index = 0 if reference_prefix == 'swmath' else 1 if reference_prefix == 'doi' else None,
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Benchmarks to Questionnaire
                    for idx, benchmark in enumerate(data.benchmarks):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Software BRelatant"]["uri"]}', 
                                     text = f"{benchmark.label} ({benchmark.description}) [{source}]", 
                                     external_id = benchmark.id, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Publications to Questionnaire
                    add_publication(instance, data.publications, source)
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
                    # Structure Results
                    data = AlgorithmicProblem.from_query(results)
                    # Load MathAlgoDB
                    mathalgodb = get_data('algorithm/data/mapping.json')
                    # Add Benchmarks to Questionnaire
                    for idx, benchmark in enumerate(data.benchmarks):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Problem BRelatant"]["uri"]}', 
                                     text = f"{benchmark.label} ({benchmark.description}) [{source}]", 
                                     external_id = benchmark.id, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Relations between Algorithmic Problems to Questionnaire
                    props = ['specializes', 'specializedBy']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Problem IntraClassRelation"]["uri"]}', 
                                         option = Option.objects.get(uri=mathalgodb[prop]), 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Problem IntraClassElement"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            idx +=1
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
                    for idx, problem in enumerate(data.problems):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Algorithm PRelatant"]["uri"]}', 
                                     text = f"{problem.label} ({problem.description}) [{source}]", 
                                     external_id = problem.id, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Softwares to Questionnaire
                    for idx, software in enumerate(data.softwares):
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Algorithm SRelatant"]["uri"]}', 
                                     text = f"{software.label} ({software.description}) [{source}]", 
                                     external_id = software.id, 
                                     collection_index = idx, 
                                     set_index = 0, 
                                     set_prefix = instance.set_index)
                    # Add Relations between Algorithms to Questionnaire
                    props = ['hasComponent', 'componentOf', 'hasSubclass', 'subclassOf', 'relatedTo']
                    idx = 0
                    for prop in props:
                        for value in getattr(data, prop):
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Algorithm IntraClassRelation"]["uri"]}', 
                                         option = Option.objects.get(uri=mathalgodb[prop]), 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            value_editor(project = instance.project, 
                                         uri = f'{BASE_URI}{questions["Algorithm IntraClassElement"]["uri"]}', 
                                         text = f"{value.label} ({value.description}) [{source}]", 
                                         external_id = value.id, 
                                         set_index = idx, 
                                         set_prefix = instance.set_index)
                            idx +=1
                    # Add Publications to Questionnaire
                    add_publication(instance, data.publications, source)
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
                ID = instance.external_id
                # Get (set) ids of exisitng benchmark in questionnaire
                set_ids = get_id(instance, f'{BASE_URI}{questions["Benchmark"]["uri"]}', ['set_index'])
                value_ids = get_id(instance, f'{BASE_URI}{questions["Benchmark ID"]["uri"]}', ['external_id'])
                # Add Benchmark entry to questionnaire
                idx = max(set_ids, default = -1) + 1
                if ID not in value_ids:
                    # Set up Page
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Benchmark"]["uri"]}', 
                                 text = f"B{idx}", 
                                 set_index = idx)
                    # Add ID Values
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Benchmark ID"]["uri"]}', 
                                 text = f'{label} ({description}) [{source}]', 
                                 external_id = ID, 
                                 set_index = idx)
                    idx += 1
                    value_ids.append(ID)

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
                ID = instance.external_id
                # Get (set) ids of exisitng benchmark in questionnaire
                set_ids = get_id(instance, f'{BASE_URI}{questions["Benchmark"]["uri"]}', ['set_index'])
                value_ids = get_id(instance, f'{BASE_URI}{questions["Benchmark ID"]["uri"]}', ['external_id'])
                # Add Benchmark entry to questionnaire
                idx = max(set_ids, default = -1) + 1
                if ID not in value_ids:
                    # Set up Page
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Benchmark"]["uri"]}', 
                                 text = f"B{idx}", 
                                 set_index = idx)
                    # Add ID Values
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Benchmark ID"]["uri"]}', 
                                 text = f'{label} ({description}) [{source}]', 
                                 external_id = ID, 
                                 set_index = idx)
                    idx += 1
                    value_ids.append(ID)

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
                ID = instance.external_id
                # Get (set) ids of exisitng problems in questionnaire
                set_ids = get_id(instance, f'{BASE_URI}{questions["Problem"]["uri"]}', ['set_index'])
                value_ids = get_id(instance, f'{BASE_URI}{questions["Problem ID"]["uri"]}', ['external_id'])
                # Add Problem entry to questionnaire
                idx = max(set_ids, default = -1) + 1
                if ID not in value_ids:
                    # Set up Page
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Problem"]["uri"]}', 
                                 text = f"AP{idx}", 
                                 set_index = idx)
                    # Add ID Values
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Problem ID"]["uri"]}', 
                                 text = f'{label} ({description}) [{source}]', 
                                 external_id = ID, 
                                 set_index = idx)
                    idx += 1
                    value_ids.append(ID)

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
                    ID = instance.external_id
                    # Get (set) ids of exisitng software in questionnaire
                    set_ids = get_id(instance, f'{BASE_URI}{questions["Software"]["uri"]}', ['set_index'])
                    value_ids = get_id(instance, f'{BASE_URI}{questions["Software ID"]["uri"]}', ['external_id'])
                    # Add Software entry to questionnaire
                    idx = max(set_ids, default = -1) + 1
                    if ID not in value_ids:
                        # Set up Page
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Software"]["uri"]}', 
                                     text = f"S{idx}", 
                                     set_index = idx)
                        # Add ID Values
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Software ID"]["uri"]}', 
                                     text = f'{label} ({description}) [{source}]', 
                                     external_id = ID, 
                                     set_index = idx)
                        idx += 1
                        value_ids.append(ID)



                
                
                