'''Module containing Handlers for the Algorithm Documentation'''

from .constants import PROPS
from .models import Benchmark, Software, Problem, Algorithm

from ..constants import BASE_URI
from ..getters import get_mathalgodb, get_questions, get_sparql_query, get_url
from ..queries import query_sparql
from ..adders import (
    add_basics,
    add_entities,
    add_relations_static,
    add_relations_flexible,
    add_references
)

class Information:
    '''Class containing functions, querying external sources for specific
       entities and integrating the related metadata into the questionnaire.'''

    def __init__(self):
        # Load shared data once
        self.questions = get_questions("algorithm") | get_questions('publication')
        self.mathalgodb = get_mathalgodb()
        self.base = BASE_URI

    def benchmark(self, instance):
        '''Benchmark Information'''

        # Benchmark specific Questions.
        benchmark = self.questions["Benchmark"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = "Benchmark",
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # If Item from MathModDB, query relations and load MathModDB Vocabulary
        query = get_sparql_query('algorithm/queries/benchmark.sparql').format(identifier)
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Get Benchmark Data from Query
        data = Benchmark.from_query(results)

        # Add References to Questionnaire
        add_references(
            project = instance.project,
            data = data,
            uri = f'{self.base}{benchmark["Reference"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add Publications to Questionnaire
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def software(self, instance):
        '''Software Information'''

        # Software specific Questions.
        software = self.questions["Software"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = "Software",
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        query = get_sparql_query('algorithm/queries/software.sparql').format(identifier)
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Results and load MathAlgoDB
        data = Software.from_query(results)

        # Add References to Questionnaire
        add_references(
            project = instance.project,
            data = data,
            uri = f'{self.base}{software["Reference"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add Benchmarks to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['S2B']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{software["BRelatant"]["uri"]}'
            }
        )

        # Add Publications to Questionnaire
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def problem(self, instance):
        '''Algorithmic Problem Information'''

        # Algorithmic Problem specific Questions.
        problem = self.questions["Problem"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = "Problem",
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        query = get_sparql_query('algorithm/queries/problem.sparql').format(identifier)
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Data and load MathAlgoDB
        data = Problem.from_query(results)

        # Add Benchmarks to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['P2B']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{problem["BRelatant"]["uri"]}'
            }
        )

        # Add Relations between Algorithmic Problems to Questionnaire
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['Problem'],
                'mapping': self.mathalgodb,
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relation': f'{self.base}{problem["IntraClassRelation"]["uri"]}',
                'relatant': f'{self.base}{problem["IntraClassElement"]["uri"]}',
            },
        )

    def algorithm(self, instance):
        '''Algorithm Information'''

        # Algorithm specific Questions.
        algorithm = self.questions["Algorithm"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = "Algorithm",
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        query = get_sparql_query('algorithm/queries/algorithm.sparql').format(identifier)
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Data and load MathAlgoDB
        data = Algorithm.from_query(results)

        # Add Algorithmic Problems to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['A2P']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{algorithm["PRelatant"]["uri"]}'
            }
        )

        # Add Softwares to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['A2S']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{algorithm["SRelatant"]["uri"]}'
            }
        )

        # Add Relations between Algorithms to Questionnaire
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['Algorithm'],
                'mapping': self.mathalgodb,
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relation': f'{self.base}{algorithm["IntraClassRelation"]["uri"]}',
                'relatant': f'{self.base}{algorithm["IntraClassElement"]["uri"]}',
            },
        )

        # Add Publications to Questionnaire
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )
