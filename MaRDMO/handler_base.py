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

from .getters import get_id
from .helpers import value_editor
from .adders import add_basics

logger = logging.getLogger(__name__)

# Lazy singleton – avoids circular import and repeated instantiation
_PUB_INFO = None


def _get_pub_info():
    global _PUB_INFO          # pylint: disable=global-statement
    if _PUB_INFO is None:
        from .publication.handlers import Information as PublicationInformation  # noqa: PLC0415
        _PUB_INFO = PublicationInformation()
    return _PUB_INFO


def _values_clause(items):
    '''Return "wd:Q1 wd:Q2 …" from a list of (text, ext_id, idx).'''
    return ' '.join(f'wd:{ext_id.split(":")[-1]}' for _, ext_id, _ in items)


class BaseInformation:
    '''Shared infrastructure for Model and Algorithm handlers.

    Subclasses must set self.questions and self.base in __init__, and
    declare _ENTITY_KEYS as a tuple of question-group keys whose ID URIs
    are collected by _collect_existing_ids.
    '''

    _ENTITY_KEYS = ()

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
        from rdmo.domain.models import Attribute  # noqa: PLC0415
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

    def _hydrate_relatants(self, project, data, prop_keys, question_id_uri,
                           question_set_uri, prefix, fill_method, catalog,
                           visited, batch_fill_method=None):
        '''Register and hydrate all relatants found under prop_keys.

        Skips ids already in visited.  Collects mardi items for a single
        batch SPARQL call when batch_fill_method is provided; otherwise
        calls fill_method individually.
        '''
        existing = get_id(project, question_set_uri, ['set_index'])
        next_idx = max((e for e in existing if e is not None), default=-1) + 1
        batch_items = []

        for prop in prop_keys:
            for relatant in getattr(data, prop, []):
                if relatant.id in visited:
                    continue
                visited.add(relatant.id)

                source = relatant.id.split(':')[0]
                text   = f'{relatant.label} ({relatant.description}) [{source}]'

                value_editor(project=project, uri=question_set_uri,
                             info={'text': f'{prefix}{next_idx + 1}',
                                   'set_index': next_idx})
                value_editor(project=project, uri=question_id_uri,
                             info={'text': text, 'external_id': relatant.id,
                                   'set_index': next_idx})

                if batch_fill_method and source == 'mardi':
                    batch_items.append((text, relatant.id, next_idx))
                else:
                    fill_method(project=project, text=text,
                                external_id=relatant.id, set_index=next_idx,
                                catalog=catalog, visited=visited)

                next_idx += 1

        if batch_items and batch_fill_method:
            batch_fill_method(project=project, items=batch_items,
                              catalog=catalog, visited=visited)

    def _fill(self, project, text, external_id, set_index,
              item_type, batch_fill_method, catalog='', visited=None):
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
        if external_id.split(':')[0] != 'mardi':
            return
        batch_fill_method(project=project, items=[(text, external_id, set_index)],
                          catalog=catalog, visited=visited)
