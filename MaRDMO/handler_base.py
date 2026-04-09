'''Shared base class for MaRDMO entity handlers.

Provides the four methods that are identical between the Model and Algorithm
Information classes:
  - _entry
  - _collect_existing_ids
  - _hydrate_relatants
  - _fill

Both handlers pass catalog through every call.  The algorithm handler
simply uses the default catalog='' everywhere.
'''

import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from .getters import (
    get_id,
    get_items,
    get_properties,
    get_sparql_query,
    get_sparql_query_optional,
    get_url,
)
from .helpers import value_editor
from .adders import add_basics
from .queries import query_sparql

logger = logging.getLogger(__name__)

# Lazy singleton – instantiated on first use so that the Django app registry
# is guaranteed to be ready (publication.handlers imports rdmo ORM models).
_PUB_INFO: list = []


def _get_pub_info():
    if not _PUB_INFO:
        from .publication.handlers import Information  # pylint: disable=import-outside-toplevel
        _PUB_INFO.append(Information())
    return _PUB_INFO[0]


@dataclass
class _RelatantSpec:
    '''Bundles section-target and call-context parameters for _hydrate_relatants.

    question_id_uri   – RDMO attribute URI for the relatant's ID field
    question_set_uri  – RDMO attribute URI for the relatant's set field
    prefix            – label prefix used when registering new set entries
    fill_method       – pre-configured callable (usually a partial of _fill)
    catalog           – current project catalog string (forwarded to fill methods)
    visited           – mutable set of already-processed external IDs
    batch_fill_method – optional batch SPARQL hydrator; when set, mardi/wikidata
                        relatants are collected and dispatched in one query
    section_indices   – optional shared dict {question_set_uri: next_idx};
                        pass the same dict to sibling calls to avoid repeated
                        DB queries for the max set_index of the same section
    '''
    question_id_uri: str
    question_set_uri: str
    prefix: str
    fill_method: Any
    catalog: str
    visited: set
    batch_fill_method: Any = None
    section_indices: Optional[dict] = field(default=None)


def _values_clause(items):
    '''Return "wd:Q1 wd:Q2 …" from a list of (text, ext_id, idx).'''
    return ' '.join(f'wd:{ext_id.split(":")[-1]}' for _, ext_id, _ in items)


def _fetch_by_source(items, mardi_file, wikidata_file, model_class):
    '''Run one SPARQL query per source; return {external_id: instance} dict.

    Uses get_sparql_query for the mardi file (always required) and
    get_sparql_query_optional for the wikidata file (no-op if absent).
    Both functions are lru_cached, so repeated calls are free.
    '''
    data_by_id     = {}
    mardi_items    = [(t, eid, si) for t, eid, si in items if eid.startswith('mardi:')]
    wikidata_items = [(t, eid, si) for t, eid, si in items if eid.startswith('wikidata:')]

    if mardi_items:
        query   = get_sparql_query(mardi_file).format(
            _values_clause(mardi_items), **get_items(), **get_properties()
        )
        results = query_sparql(query, get_url('mardi', 'sparql'))
        if results:
            data_by_id.update(model_class.from_query_batch(results))

    if wikidata_items:
        tmpl = get_sparql_query_optional(wikidata_file)
        if tmpl:
            query   = tmpl.format(
                _values_clause(wikidata_items), **get_items(), **get_properties()
            )
            results = query_sparql(query, get_url('wikidata', 'sparql'))
            if results:
                data_by_id.update(model_class.from_query_batch(results))

    return data_by_id


class BaseInformation:  # pylint: disable=too-few-public-methods
    '''Shared infrastructure for Model and Algorithm handlers.

    Subclasses must set self.questions and self.base in __init__, and
    declare _ENTITY_KEYS as a tuple of question-group keys whose ID URIs
    are collected by _collect_existing_ids.
    '''

    # Declared here so pylint and type checkers know these attributes exist;
    # concrete values are assigned by each subclass __init__.
    base: str
    questions: dict

    _ENTITY_KEYS: tuple = ()

    def _entry(self, instance, item_type, batch_fill_method):
        '''Common entry-point: build visited set, call _fill.'''
        visited = self._collect_existing_ids(instance.project)
        self._fill(
            project           = instance.project,
            text              = instance.text,
            external_id       = instance.external_id,
            set_index         = instance.set_index,
            item_type         = item_type,
            batch_fill_method = batch_fill_method,
            catalog           = str(getattr(instance.project, 'catalog', '')),
            visited           = visited,
        )

    def _collect_existing_ids(self, project):
        '''Single batched DB query for all external_ids already in the
        questionnaire across all entity sections.'''
        from rdmo.domain.models import Attribute  # pylint: disable=import-outside-toplevel
        id_uris = [
            f'{self.base}{self.questions[k]["ID"]["uri"]}'
            for k in self._ENTITY_KEYS
        ]
        attr_ids = Attribute.objects.filter(uri__in=id_uris).values_list('id', flat=True)
        return set(
            project.values.filter(
                snapshot=None,
                attribute_id__in=attr_ids,
                external_id__isnull=False,
            ).exclude(external_id='').values_list('external_id', flat=True)
        )

    def _hydrate_relatants(self, project, data, prop_keys, spec):
        '''Register and hydrate all relatants found under prop_keys.

        See _RelatantSpec for full parameter documentation.  Skips IDs
        already in spec.visited.  Collects mardi/wikidata items for a
        single batch SPARQL call when spec.batch_fill_method is set;
        otherwise falls back to spec.fill_method per relatant.
        '''
        if spec.section_indices is not None and spec.question_set_uri in spec.section_indices:
            next_idx = spec.section_indices[spec.question_set_uri]
        else:
            existing = get_id(project, spec.question_set_uri, ['set_index'])
            next_idx = max((e for e in existing if e is not None), default=-1) + 1

        batch_items = []

        for prop in prop_keys:
            for relatant in getattr(data, prop, []):
                if relatant.id in spec.visited:
                    continue
                spec.visited.add(relatant.id)

                source = relatant.id.split(':')[0]
                text   = f'{relatant.label} ({relatant.description}) [{source}]'

                value_editor(project=project, uri=spec.question_set_uri,
                             info={'text': f'{spec.prefix}{next_idx + 1}',
                                   'set_index': next_idx})
                value_editor(project=project, uri=spec.question_id_uri,
                             info={'text': text, 'external_id': relatant.id,
                                   'set_index': next_idx})

                if spec.batch_fill_method and source in ('mardi', 'wikidata'):
                    batch_items.append((text, relatant.id, next_idx))
                else:
                    spec.fill_method(project=project, text=text,
                                     external_id=relatant.id, set_index=next_idx,
                                     catalog=spec.catalog, visited=spec.visited)

                next_idx += 1

        if spec.section_indices is not None:
            spec.section_indices[spec.question_set_uri] = next_idx

        if batch_items and spec.batch_fill_method:
            spec.batch_fill_method(project=project, items=batch_items,
                                   catalog=spec.catalog, visited=spec.visited)

    def _hydrate_publications(self, project, publications, catalog, visited):
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

            source = pub.id.split(':')[0]
            text   = f'{pub.label} ({pub.description}) [{source}]'
            value_editor(project=project, uri=pub_set_uri,
                         info={'text': f'P{next_idx + 1}', 'set_index': next_idx})
            value_editor(project=project, uri=pub_id_uri,
                         info={'text': text, 'external_id': pub.id,
                               'set_index': next_idx})

            pub_info.fill_citation(project=project, text=text,
                                   external_id=pub.id, set_index=next_idx,
                                   catalog=catalog)
            next_idx += 1

    def _fill(
        self, project, text, external_id, set_index,
        item_type, batch_fill_method, catalog='', visited=None
    ):
        '''Guard, add_basics for non-mardi items, delegate to batch_fill_method.

        item_type         – questionnaire item type string
        batch_fill_method – corresponding _fill_*_batch method to delegate to
        '''
        if not text or text == 'not found':
            return
        if visited is None:
            visited = set()
        visited.add(external_id)
        add_basics(project=project, text=text, questions=self.questions,
                   item_type=item_type, index=(0, set_index))
        if external_id.split(':')[0] not in ('mardi', 'wikidata'):
            return
        batch_fill_method(project=project, items=[(text, external_id, set_index)],
                          catalog=catalog, visited=visited)
