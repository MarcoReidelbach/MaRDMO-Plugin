'''Module containing Handlers for the Algorithm Documentation.

Information inherits _entry, _collect_existing_ids, _hydrate_relatants,
and _fill from BaseInformation (MaRDMO/base_handler.py).

All batch methods accept catalog='' (unused but required by the shared
_fill and _hydrate_relatants signatures).
'''

import logging
from functools import partial

from .constants import PROPS
from .models import Benchmark, Software, Problem, Algorithm

from ..handler_base import BaseInformation, _get_pub_info, _values_clause
from ..constants import BASE_URI
from ..getters import (
    get_id,
    get_items,
    get_mathalgodb,
    get_properties,
    get_questions,
    get_sparql_query,
    get_sparql_query_optional,
    get_url,
)
from ..helpers import value_editor
from ..queries import query_sparql
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
        self._entry(instance, 'Benchmark', self._fill_benchmark_batch)

    def software(self, instance):
        self._entry(instance, 'Software', self._fill_software_batch)

    def problem(self, instance):
        self._entry(instance, 'Problem', self._fill_problem_batch)

    def algorithm(self, instance):
        self._entry(instance, 'Algorithm', self._fill_algorithm_batch)

    # ------------------------------------------------------------------ #
    #  Algorithm-specific cascade helper                                   #
    # ------------------------------------------------------------------ #

    def _hydrate_publications(self, project, publications, source, catalog, visited):
        '''Register and hydrate publications via the publication handler.'''
        pub_info    = _get_pub_info()
        pub_id_uri  = f'{self.base}{self.questions["Publication"]["ID"]["uri"]}'
        pub_set_uri = f'{self.base}{self.questions["Publication"]["uri"]}'

        existing = get_id(project, pub_set_uri, ['set_index'])
        next_idx = max((e for e in existing if e is not None), default=-1) + 1

        for pub in publications:
            if pub.id in visited:
                continue
            visited.add(pub.id)

            text = f'{pub.label} ({pub.description}) [{source}]'
            value_editor(project=project, uri=pub_set_uri,
                         info={'text': f'P{next_idx + 1}', 'set_index': next_idx})
            value_editor(project=project, uri=pub_id_uri,
                         info={'text': text, 'external_id': pub.id,
                               'set_index': next_idx})

            pub_info._fill_citation(project=project, text=text,
                                    external_id=pub.id, set_index=next_idx,
                                    catalog=catalog)
            next_idx += 1

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
        data_by_id = {}

        mardi_items    = [(t, eid, si) for t, eid, si in items if eid.startswith('mardi:')]
        wikidata_items = [(t, eid, si) for t, eid, si in items if eid.startswith('wikidata:')]

        if mardi_items:
            query   = get_sparql_query('algorithm/queries/benchmark_mardi.sparql').format(
                _values_clause(mardi_items), **get_items(), **get_properties()
            )
            results = query_sparql(query, get_url('mardi', 'sparql'))
            if results:
                data_by_id.update(Benchmark.from_query_batch(results))

        if wikidata_items:
            tmpl = get_sparql_query_optional('algorithm/queries/benchmark_wikidata.sparql')
            if tmpl:
                query   = tmpl.format(
                    _values_clause(wikidata_items), **get_items(), **get_properties()
                )
                results = query_sparql(query, get_url('wikidata', 'sparql'))
                if results:
                    data_by_id.update(Benchmark.from_query_batch(results))

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

            self._hydrate_publications(project, data.publications, 'mardi',
                                       catalog, visited)

    def _fill_software_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple software items with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        software   = self.questions['Software']
        data_by_id = {}

        mardi_items    = [(t, eid, si) for t, eid, si in items if eid.startswith('mardi:')]
        wikidata_items = [(t, eid, si) for t, eid, si in items if eid.startswith('wikidata:')]

        if mardi_items:
            query   = get_sparql_query('algorithm/queries/software_mardi.sparql').format(
                _values_clause(mardi_items), **get_items(), **get_properties()
            )
            results = query_sparql(query, get_url('mardi', 'sparql'))
            if results:
                data_by_id.update(Software.from_query_batch(results))

        if wikidata_items:
            tmpl = get_sparql_query_optional('algorithm/queries/software_wikidata.sparql')
            if tmpl:
                query   = tmpl.format(
                    _values_clause(wikidata_items), **get_items(), **get_properties()
                )
                results = query_sparql(query, get_url('wikidata', 'sparql'))
                if results:
                    data_by_id.update(Software.from_query_batch(results))

        if not data_by_id:
            return

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
                question_id_uri=f'{self.base}{self.questions["Benchmark"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Benchmark"]["uri"]}',
                prefix='B',
                fill_method=partial(self._fill, item_type='Benchmark',
                                    batch_fill_method=self._fill_benchmark_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_benchmark_batch)

            self._hydrate_publications(project, data.publications, 'mardi',
                                       catalog, visited)

    def _fill_problem_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple algorithmic problems with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        problem    = self.questions['Problem']
        data_by_id = {}

        mardi_items    = [(t, eid, si) for t, eid, si in items if eid.startswith('mardi:')]
        wikidata_items = [(t, eid, si) for t, eid, si in items if eid.startswith('wikidata:')]

        if mardi_items:
            query   = get_sparql_query('algorithm/queries/problem_mardi.sparql').format(
                _values_clause(mardi_items), **get_items(), **get_properties()
            )
            results = query_sparql(query, get_url('mardi', 'sparql'))
            if results:
                data_by_id.update(Problem.from_query_batch(results))

        if wikidata_items:
            tmpl = get_sparql_query_optional('algorithm/queries/problem_wikidata.sparql')
            if tmpl:
                query   = tmpl.format(
                    _values_clause(wikidata_items), **get_items(), **get_properties()
                )
                results = query_sparql(query, get_url('wikidata', 'sparql'))
                if results:
                    data_by_id.update(Problem.from_query_batch(results))

        if not data_by_id:
            return

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
                question_id_uri=f'{self.base}{self.questions["Benchmark"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Benchmark"]["uri"]}',
                prefix='B',
                fill_method=partial(self._fill, item_type='Benchmark',
                                    batch_fill_method=self._fill_benchmark_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_benchmark_batch)

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
        data_by_id = {}

        mardi_items    = [(t, eid, si) for t, eid, si in items if eid.startswith('mardi:')]
        wikidata_items = [(t, eid, si) for t, eid, si in items if eid.startswith('wikidata:')]

        if mardi_items:
            query   = get_sparql_query('algorithm/queries/algorithm_mardi.sparql').format(
                _values_clause(mardi_items), **get_items(), **get_properties()
            )
            results = query_sparql(query, get_url('mardi', 'sparql'))
            if results:
                data_by_id.update(Algorithm.from_query_batch(results))

        if wikidata_items:
            tmpl = get_sparql_query_optional('algorithm/queries/algorithm_wikidata.sparql')
            if tmpl:
                query   = tmpl.format(
                    _values_clause(wikidata_items), **get_items(), **get_properties()
                )
                results = query_sparql(query, get_url('wikidata', 'sparql'))
                if results:
                    data_by_id.update(Algorithm.from_query_batch(results))

        if not data_by_id:
            return

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
                question_id_uri=f'{self.base}{self.questions["Problem"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Problem"]["uri"]}',
                prefix='AT',
                fill_method=partial(self._fill, item_type='Problem',
                                    batch_fill_method=self._fill_problem_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_problem_batch)

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['A2S']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{algorithm["SRelatant"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['A2S'],
                question_id_uri=f'{self.base}{self.questions["Software"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Software"]["uri"]}',
                prefix='S',
                fill_method=partial(self._fill, item_type='Software',
                                    batch_fill_method=self._fill_software_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_software_batch)

            add_relations_flexible(
                project=project, data=data,
                props={'keys': PROPS['Algorithm'], 'mapping': self.mathalgodb},
                index={'set_prefix': set_index},
                statement={
                    'relation': f'{self.base}{algorithm["IntraClassRelation"]["uri"]}',
                    'relatant': f'{self.base}{algorithm["IntraClassElement"]["uri"]}',
                })

            self._hydrate_publications(project, data.publications, 'mardi',
                                       catalog, visited)