'''Module containing Handlers for the Workflow Documentation.

Information inherits _entry, _collect_existing_ids, _hydrate_relatants,
and _fill from BaseInformation (MaRDMO/handler_base.py).
'''

import logging
from functools import partial

from ..handler_base import BaseInformation, _RelatantSpec, _fetch_by_source
from ..constants import BASE_URI
from ..getters import get_options, get_questions
from ..helpers import value_editor
from ..adders import add_basics, add_references, add_relations_static

from .constants import PROPS
from .models import Method, ProcessStep, Software, Hardware, DataSet

logger = logging.getLogger(__name__)


class Information(BaseInformation):
    '''Handlers for the Workflow Documentation questionnaire.'''

    _ENTITY_KEYS = ('Software', 'Hardware', 'Instrument', 'Data Set', 'Method', 'Process Step')

    def __init__(self):
        self.questions = get_questions('workflow')
        self.base      = BASE_URI
        self.options   = get_options()

    # ------------------------------------------------------------------ #
    #  Public entry points (called by router via post_save signal)         #
    # ------------------------------------------------------------------ #

    def software(self, instance):
        '''Handle Software ID save: hydrate basics and SPARQL data.'''
        self._entry(instance, 'Software', self._fill_software_batch)

    def hardware(self, instance):
        '''Handle Hardware ID save: hydrate basics and SPARQL data.'''
        self._entry(instance, 'Hardware', self._fill_hardware_batch)

    def instrument(self, instance):
        '''Handle Instrument ID save: hydrate basics only (no SPARQL).'''
        self._entry(instance, 'Instrument', self._fill_instrument_batch)

    def data_set(self, instance):
        '''Handle Data Set ID save: hydrate basics and SPARQL data.'''
        self._entry(instance, 'Data Set', self._fill_data_set_batch)

    def method(self, instance):
        '''Handle Method ID save: hydrate basics and cascade to Software/Instrument.'''
        self._entry(instance, 'Method', self._fill_method_batch)

    def process_step(self, instance):
        '''Handle Process Step ID save: hydrate basics and cascade to all related entities.'''
        self._entry(instance, 'Process Step', self._fill_process_step_batch)

    # ------------------------------------------------------------------ #
    #  Batch _fill_* methods (one SPARQL query for N entities)            #
    # ------------------------------------------------------------------ #

    def _fill_software_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple software items with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        software   = self.questions['Software']
        data_by_id = _fetch_by_source(
            items,
            'workflow/queries/software_mardi.sparql',
            'workflow/queries/software_wikidata.sparql',
            Software,
        )

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
                props={'keys': PROPS['S2PL']},
                index={'set_prefix': set_index},
                statement={
                    'relatant': f'{self.base}{software["Programming Language"]["uri"]}'
                })

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['S2DP']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{software["Dependency"]["uri"]}'})

    def _fill_hardware_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple hardware items with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        hardware   = self.questions['Hardware']
        data_by_id = _fetch_by_source(
            items,
            'workflow/queries/hardware_mardi.sparql',
            'workflow/queries/hardware_wikidata.sparql',
            Hardware,
        )

        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Hardware', index=(0, set_index))

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['H2CPU']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{hardware["CPU"]["uri"]}'})

            if data.nodes:
                value_editor(
                    project=project,
                    uri=f'{self.base}{hardware["Nodes"]["uri"]}',
                    info={'text': data.nodes, 'set_prefix': set_index})

            if data.cores:
                value_editor(
                    project=project,
                    uri=f'{self.base}{hardware["Cores"]["uri"]}',
                    info={'text': data.cores, 'set_prefix': set_index})

    def _fill_instrument_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple instruments. Instruments have no external SPARQL data.'''
        if not items:
            return

        for text, _, set_index in items:
            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Instrument', index=(0, set_index))

    def _fill_data_set_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple data sets with a single SPARQL query per source.'''
        if not items:
            return
        if visited is None:
            visited = set()

        data_set_q = self.questions['Data Set']
        data_by_id = _fetch_by_source(
            items,
            'workflow/queries/data_set_mardi.sparql',
            'workflow/queries/data_set_wikidata.sparql',
            DataSet,
        )

        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue
            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Data Set', index=(0, set_index))
            self._write_data_set_fields(project, data_set_q, data, set_index)

    def _write_data_set_fields(self, project, data_set_q, data, set_index):
        '''Write all RDMO fields for one data set item.'''
        if data.size:
            value_editor(
                project=project,
                uri=f'{self.base}{data_set_q["Size"]["uri"]}',
                info={'text': data.size[1], 'option': data.size[0],
                      'set_prefix': set_index})

        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['DS2DT']},
            index={'set_prefix': set_index},
            statement={
                'relatant': f'{self.base}{data_set_q["Data Type"]["uri"]}'
            })

        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['DS2RF']},
            index={'set_prefix': set_index},
            statement={
                'relatant': f'{self.base}{data_set_q["Representation Format"]["uri"]}'
            })

        if data.file_format:
            value_editor(
                project=project,
                uri=f'{self.base}{data_set_q["File Format"]["uri"]}',
                info={'text': data.file_format, 'set_prefix': set_index})

        if data.binary_or_text:
            value_editor(
                project=project,
                uri=f'{self.base}{data_set_q["Binary or Text"]["uri"]}',
                info={'option': data.binary_or_text, 'set_prefix': set_index})

        if data.proprietary:
            value_editor(
                project=project,
                uri=f'{self.base}{data_set_q["Proprietary"]["uri"]}',
                info={'option': data.proprietary, 'set_prefix': set_index})

        add_references(project=project, data=data,
                       uri=f'{self.base}{data_set_q["To Publish"]["uri"]}',
                       set_prefix=set_index)

        if data.to_archive:
            value_editor(
                project=project,
                uri=f'{self.base}{data_set_q["To Archive"]["uri"]}',
                info={'text': data.to_archive[1], 'option': data.to_archive[0],
                      'set_prefix': set_index})

    def _fill_method_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple methods with a single SPARQL query per source.

        Explicitly cascades into Software and Instrument via _hydrate_relatants.
        '''
        if not items:
            return
        if visited is None:
            visited = set()

        method     = self.questions['Method']
        data_by_id = _fetch_by_source(
            items,
            'workflow/queries/method_mardi.sparql',
            'workflow/queries/method_wikidata.sparql',
            Method,
        )

        section_indices = {}
        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Method', index=(0, set_index))

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['M2S']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{method["Software"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['M2S'],
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

            add_relations_static(
                project=project, data=data,
                props={'keys': PROPS['M2I']},
                index={'set_prefix': set_index},
                statement={'relatant': f'{self.base}{method["Instrument"]["uri"]}'})

            self._hydrate_relatants(
                project=project, data=data, prop_keys=PROPS['M2I'],
                spec=_RelatantSpec(
                    question_id_uri=f'{self.base}{self.questions["Instrument"]["ID"]["uri"]}',
                    question_set_uri=f'{self.base}{self.questions["Instrument"]["uri"]}',
                    prefix='I',
                    fill_method=partial(self._fill, item_type='Instrument',
                                        batch_fill_method=self._fill_instrument_batch),
                    catalog=catalog, visited=visited,
                    batch_fill_method=self._fill_instrument_batch,
                    section_indices=section_indices,
                ))

    def _fill_process_step_batch(self, project, items, catalog='', visited=None):
        '''Hydrate multiple process steps with a single SPARQL query per source.

        Explicitly cascades into Data Set, Method, Software, and Instrument
        via _hydrate_relatants instead of relying on signal-driven cascades.
        '''
        if not items:
            return
        if visited is None:
            visited = set()

        process_step = self.questions['Process Step']
        data_by_id   = _fetch_by_source(
            items,
            'workflow/queries/process_step_mardi.sparql',
            'workflow/queries/process_step_wikidata.sparql',
            ProcessStep,
        )

        section_indices = {}
        for text, external_id, set_index in items:
            data = data_by_id.get(external_id)
            if not data:
                continue

            add_basics(project=project, text=text, questions=self.questions,
                       item_type='Process Step', index=(0, set_index))

            self._fill_process_step_relations(
                project, process_step, data, set_index, catalog, visited,
                section_indices,
            )

    def _fill_process_step_relations(
        self, project, process_step, data, set_index, catalog, visited,
        section_indices=None,
    ):
        '''Write all relation fields and cascade hydration for one process step.'''
        # Input Data Sets
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2IDS']},
            index={'set_prefix': set_index},
            statement={'relatant': f'{self.base}{process_step["Input"]["uri"]}'})

        self._hydrate_relatants(
            project=project, data=data, prop_keys=PROPS['PS2IDS'],
            spec=_RelatantSpec(
                question_id_uri=f'{self.base}{self.questions["Data Set"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Data Set"]["uri"]}',
                prefix='DS',
                fill_method=partial(self._fill, item_type='Data Set',
                                    batch_fill_method=self._fill_data_set_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_data_set_batch,
                section_indices=section_indices,
            ))

        # Output Data Sets
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2ODS']},
            index={'set_prefix': set_index},
            statement={'relatant': f'{self.base}{process_step["Output"]["uri"]}'})

        self._hydrate_relatants(
            project=project, data=data, prop_keys=PROPS['PS2ODS'],
            spec=_RelatantSpec(
                question_id_uri=f'{self.base}{self.questions["Data Set"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Data Set"]["uri"]}',
                prefix='DS',
                fill_method=partial(self._fill, item_type='Data Set',
                                    batch_fill_method=self._fill_data_set_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_data_set_batch,
                section_indices=section_indices,
            ))

        # Methods
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2M']},
            index={'set_prefix': set_index},
            statement={'relatant': f'{self.base}{process_step["Method"]["uri"]}'})

        self._hydrate_relatants(
            project=project, data=data, prop_keys=PROPS['PS2M'],
            spec=_RelatantSpec(
                question_id_uri=f'{self.base}{self.questions["Method"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Method"]["uri"]}',
                prefix='M',
                fill_method=partial(self._fill, item_type='Method',
                                    batch_fill_method=self._fill_method_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_method_batch,
                section_indices=section_indices,
            ))

        # Platform Software
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2PLS']},
            index={'set_prefix': set_index},
            statement={
                'relatant':
                    f'{self.base}{process_step["Environment-Software"]["uri"]}'
            })

        self._hydrate_relatants(
            project=project, data=data, prop_keys=PROPS['PS2PLS'],
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

        # Platform Instrument
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2PLI']},
            index={'set_prefix': set_index},
            statement={
                'relatant':
                    f'{self.base}{process_step["Environment-Instrument"]["uri"]}'
            })

        self._hydrate_relatants(
            project=project, data=data, prop_keys=PROPS['PS2PLI'],
            spec=_RelatantSpec(
                question_id_uri=f'{self.base}{self.questions["Instrument"]["ID"]["uri"]}',
                question_set_uri=f'{self.base}{self.questions["Instrument"]["uri"]}',
                prefix='I',
                fill_method=partial(self._fill, item_type='Instrument',
                                    batch_fill_method=self._fill_instrument_batch),
                catalog=catalog, visited=visited,
                batch_fill_method=self._fill_instrument_batch,
                section_indices=section_indices,
            ))

        # Fields of Work (static, no cascade)
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2F']},
            index={'set_prefix': set_index},
            statement={'relatant': f'{self.base}{process_step["Discipline"]["uri"]}'})

        # MSC IDs (static, no cascade)
        add_relations_static(
            project=project, data=data,
            props={'keys': PROPS['PS2MA']},
            index={'set_prefix': set_index},
            statement={'relatant': f'{self.base}{process_step["Discipline"]["uri"]}'})
