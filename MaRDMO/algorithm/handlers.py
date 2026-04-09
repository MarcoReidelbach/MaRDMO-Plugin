'''Module containing Handlers for the Algorithm Documentation.

Information inherits _entry, _collect_existing_ids, _hydrate_relatants,
and _fill from BaseInformation (MaRDMO/handler_base.py).

All batch methods accept catalog='' (unused but required by the shared
_fill and _hydrate_relatants signatures).
'''

import logging
from functools import partial

from .constants import PROPS
from .models import Benchmark, Software, Problem, Algorithm

from ..handler_base import BaseInformation, _RelatantSpec, _fetch_by_source
from ..constants import BASE_URI
from ..getters import (
    get_mathalgodb,
    get_questions,
)
from ..adders import (
    add_basics,
    add_references,
    add_relations_flexible,
    add_relations_static,
)

logger = logging.getLogger(__name__)


class Information(BaseInformation):
    '''Handlers for the Algorithm Documentation questionnaire.'''

    _ENTITY_KEYS = ('Algorithm', 'Problem', 'Software', 'Benchmark', 'Publication')

    def __init__(self):
        self.questions  = get_questions('algorithm') | get_questions('publication')
        self.mathalgodb = get_mathalgodb()
        self.base       = BASE_URI

    # ------------------------------------------------------------------ #
    #  Public entry points (called by router via post_save signal)         #
    # ------------------------------------------------------------------ #

    def benchmark(self, instance):
        '''Handle Benchmark ID save: hydrate basics and SPARQL data.'''
        self._entry(instance, 'Benchmark', self._fill_benchmark_batch)

    def software(self, instance):
        '''Handle Software ID save: hydrate basics and cascade to Benchmark.'''
        self._entry(instance, 'Software', self._fill_software_batch)

    def problem(self, instance):
        '''Handle Problem ID save: hydrate basics and cascade to Benchmark.'''
        self._entry(instance, 'Problem', self._fill_problem_batch)

    def algorithm(self, instance):
        '''Handle Algorithm ID save: hydrate basics and cascade to Problem and Software.'''
        self._entry(instance, 'Algorithm', self._fill_algorithm_batch)

    # ------------------------------------------------------------------ #
    #  Batch _fill_* methods (one SPARQL query for N entities)            #
    # ------------------------------------------------------------------ #

    def _fill_benchmark_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple benchmarks with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        benchmark  = self.questions['Benchmark']
        data_by_id = _fetch_by_source(
            items,
            'algorithm/queries/benchmark_mardi.sparql',
            'algorithm/queries/benchmark_wikidata.sparql',
            Benchmark,
        )
        if not data_by_id:
            return

        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Benchmark', index=(0, set_index))

            add_references(project=project, data=data,
                           uri=f'{self.base}{benchmark["Reference"]["uri"]}',
                           set_prefix=set_index)

            self._hydrate_publications(project, data.publications,
                                       catalog, visited)

    def _fill_software_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple software items with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        software   = self.questions['Software']
        data_by_id = _fetch_by_source(
            items,
            'algorithm/queries/software_mardi.sparql',
            'algorithm/queries/software_wikidata.sparql',
            Software,
        )
        if not data_by_id:
            return

        section_indices = {}
        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Software', index=(0, set_index))

            add_references(project=project, data=data,
                           uri=f'{self.base}{software["Reference"]["uri"]}',
                           set_prefix=set_index)

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['S2B']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{software["BRelatant"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['S2B'],
                spec=_RelatantSpec(
                    question_id_uri=f'{self.base}{self.questions["Benchmark"]["ID"]["uri"]}',
                    question_set_uri=f'{self.base}{self.questions["Benchmark"]["uri"]}',
                    prefix='B',
                    fill_method=partial(self._fill, item_type='Benchmark',
                                        batch_fill_method=self._fill_benchmark_batch),
                    catalog=catalog, visited=visited,
                    batch_fill_method=self._fill_benchmark_batch,
                    section_indices=section_indices,
                ))

            self._hydrate_publications(project, data.publications,
                                       catalog, visited)

    def _fill_problem_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple algorithmic problems with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        problem    = self.questions['Problem']
        data_by_id = _fetch_by_source(
            items,
            'algorithm/queries/problem_mardi.sparql',
            'algorithm/queries/problem_wikidata.sparql',
            Problem,
        )
        if not data_by_id:
            return

        section_indices = {}
        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Problem', index=(0, set_index))

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['P2B']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{problem["BRelatant"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['P2B'],
                spec=_RelatantSpec(
                    question_id_uri=f'{self.base}{self.questions["Benchmark"]["ID"]["uri"]}',
                    question_set_uri=f'{self.base}{self.questions["Benchmark"]["uri"]}',
                    prefix='B',
                    fill_method=partial(self._fill, item_type='Benchmark',
                                        batch_fill_method=self._fill_benchmark_batch),
                    catalog=catalog, visited=visited,
                    batch_fill_method=self._fill_benchmark_batch,
                    section_indices=section_indices,
                ))

            add_relations_flexible(
                project=project, data=data,
                props={'keys': PROPS['Problem'], 'mapping': self.mathalgodb},
                index={'set_prefix': set_index},
                statement={
                    'relation': f'{self.base}{problem["IntraClassRelation"]["uri"]}',
                    'relatant': f'{self.base}{problem["IntraClassElement"]["uri"]}',
                })

            # IntraClass relations are not cascade-hydrated

    def _fill_algorithm_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple algorithms with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        algorithm  = self.questions['Algorithm']
        data_by_id = _fetch_by_source(
            items,
            'algorithm/queries/algorithm_mardi.sparql',
            'algorithm/queries/algorithm_wikidata.sparql',
            Algorithm,
        )
        if not data_by_id:
            return

        section_indices = {}
        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Algorithm', index=(0, set_index))

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['A2P']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{algorithm["PRelatant"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['A2P'],
                spec=_RelatantSpec(
                    question_id_uri=f'{self.base}{self.questions["Problem"]["ID"]["uri"]}',
                    question_set_uri=f'{self.base}{self.questions["Problem"]["uri"]}',
                    prefix='AT',
                    fill_method=partial(self._fill, item_type='Problem',
                                        batch_fill_method=self._fill_problem_batch),
                    catalog=catalog, visited=visited,
                    batch_fill_method=self._fill_problem_batch,
                    section_indices=section_indices,
                ))

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['A2S']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{algorithm["SRelatant"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['A2S'],
                spec=_RelatantSpec(
                    question_id_uri=f'{self.base}{self.questions["Software"]["ID"]["uri"]}',
                    question_set_uri=f'{self.base}{self.questions["Software"]["uri"]}',
                    prefix='S',
                    fill_method=partial(self._fill, item_type='Software',
                                        batch_fill_method=self._fill_software_batch),
                    catalog=catalog, visited=visited,
                    batch_fill_method=self._fill_software_batch,
                    section_indices=section_indices,
                ))

            add_relations_flexible(
                project=project, data=data,
                props={'keys': PROPS['Algorithm'], 'mapping': self.mathalgodb},
                index={'set_prefix': set_index},
                statement={
                    'relation': f'{self.base}{algorithm["IntraClassRelation"]["uri"]}',
                    'relatant': f'{self.base}{algorithm["IntraClassElement"]["uri"]}',
                })

            self._hydrate_publications(project, data.publications,
                                       catalog, visited)
