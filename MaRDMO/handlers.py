'''Module containing general Handlers for MaRDMO'''

from .adders import add_entities, add_new_entities
from .getters import get_id
from .helpers import extract_parts
from .models import Relatant

from .algorithm.constants import get_uri_prefix_map as get_uri_prefix_map_algorithm
from .model.constants import get_uri_prefix_map as get_uri_prefix_map_model
from .workflow.constants import get_uri_prefix_map as get_uri_prefix_map_workflow

# Lazy singletons – avoid circular imports and repeated instantiation
_MODEL_INFO    = None
_ALGO_INFO     = None
_WORKFLOW_INFO = None


def _get_model_info():
    global _MODEL_INFO
    if _MODEL_INFO is None:
        from .model.handlers import Information as M
        _MODEL_INFO = M()
    return _MODEL_INFO


def _get_algo_info():
    global _ALGO_INFO
    if _ALGO_INFO is None:
        from .algorithm.handlers import Information as A
        _ALGO_INFO = A()
    return _ALGO_INFO


def _get_workflow_info():
    global _WORKFLOW_INFO
    if _WORKFLOW_INFO is None:
        from .workflow.handlers import Information as W
        _WORKFLOW_INFO = W()
    return _WORKFLOW_INFO


# Map prefix → (item_type, batch_method_name) per catalog family.
_MODEL_PREFIX_TO_FILL = {
    'AD':  ('Research Field',          '_fill_field_batch'),
    'RP':  ('Research Problem',        '_fill_problem_batch'),
    'CT':  ('Task',                    '_fill_task_batch'),
    'ME':  ('Mathematical Formulation','_fill_formulation_batch'),
    'QQK': ('Quantity',                '_fill_quantity_batch'),
}

_ALGO_PREFIX_TO_FILL = {
    'AT': ('Problem',   '_fill_problem_batch'),
    'S':  ('Software',  '_fill_software_batch'),
    'B':  ('Benchmark', '_fill_benchmark_batch'),
}

_WORKFLOW_PREFIX_TO_FILL = {
    'DS': ('Data Set',   '_fill_data_set_batch'),
    'M':  ('Method',     '_fill_method_batch'),
    'S':  ('Software',   '_fill_software_batch'),
    'I':  ('Instrument', '_fill_instrument_batch'),
}

# Dispatch table: catalog suffix → (get_uri_prefix_map_fn, prefix_map, get_info_fn)
# All catalogs accept both 'mardi' and 'wikidata' as hydration sources.
_CATALOG_DISPATCH = {
    'mardmo-model-catalog': (
        get_uri_prefix_map_model,
        _MODEL_PREFIX_TO_FILL,
        _get_model_info
    ),
    'mardmo-model-basics-catalog': (
        get_uri_prefix_map_model,
        _MODEL_PREFIX_TO_FILL,
        _get_model_info
    ),
    'mardmo-interdisciplinary-workflow-catalog': (
        get_uri_prefix_map_workflow,
        _WORKFLOW_PREFIX_TO_FILL,
        _get_workflow_info
    ),
    'mardmo-algorithm-catalog': (
        get_uri_prefix_map_algorithm,
        _ALGO_PREFIX_TO_FILL,
        _get_algo_info
    ),
}


class Information:
    '''Class containing functions, querying external sources for specific
       entities and integrating the related metadata into the questionnaire.'''

    def __init__(self):
        pass

    def relation(self, instance):
        '''Relation Information.

        1. Adds the related entity to the correct questionnaire section.
        2. Explicitly hydrates the entity via _fill on the appropriate
           Information class.
        '''
        catalog_str = str(instance.project.catalog)
        catalog_key = catalog_str.rsplit('/', maxsplit=1)[-1]

        dispatch = _CATALOG_DISPATCH.get(catalog_key)
        if dispatch is None:
            return
        get_uri_prefix_map, prefix_map, get_info = dispatch

        if not instance.text:
            return

        label, description, source = extract_parts(instance.text)
        config = get_uri_prefix_map()[instance.attribute.uri]
        datas  = [Relatant.from_triple(instance.external_id, label, description)]

        # --- Step 1: add entity to questionnaire section ---
        if source in ('mardi', 'wikidata'):
            add_entities(
                project      = instance.project,
                question_set = config["question_set"],
                datas        = datas,
                source       = source,
                prefix       = config["prefix"],
            )
        elif source == 'user':
            add_new_entities(
                project      = instance.project,
                question_set = config["question_set"],
                datas        = datas,
                prefix       = config["prefix"],
            )
            return  # user-defined entities have no external data to hydrate

        # --- Step 2: explicitly hydrate the entity ---
        # Only mardi/wikidata-sourced entities carry SPARQL-queryable metadata.
        if source not in ('mardi', 'wikidata'):
            return

        entry = prefix_map.get(config["prefix"])
        if not entry:
            return
        item_type, batch_method_name = entry

        info     = get_info()
        batch_fn = getattr(info, batch_method_name)

        visited    = info._collect_existing_ids(instance.project)
        id_entries = get_id(instance.project, config["question_id"],
                            ['set_index', 'external_id'])

        for set_index, ext_id in id_entries:
            if ext_id == instance.external_id:
                info._fill(
                    project           = instance.project,
                    text              = instance.text,
                    external_id       = instance.external_id,
                    set_index         = set_index,
                    item_type         = item_type,
                    batch_fill_method = batch_fn,
                    catalog           = catalog_key,
                    visited           = visited,
                )
                break
