'''Module containing general Handlers for MaRDMO'''

from .adders import add_entities, add_new_entities
from .helpers import extract_parts
from .models import Relatant

from .algorithm.constants import get_uri_prefix_map as get_uri_prefix_map_algorithm
from .model.constants import get_uri_prefix_map as get_uri_prefix_map_model
from .workflow.constants import get_uri_prefix_map as get_uri_prefix_map_workflow

class Information:
    '''Class containing functions, querying external sources for specific
       entities and integrating the related metadata into the questionnaire.'''

    def __init__(self):
        # Load shared data once
        return

    def relation(self, instance):
        '''Relation Information'''

        # Get appropriate config map
        if str(instance.project.catalog).endswith("mardmo-model-catalog"):
            config_map = get_uri_prefix_map_model()
        elif str(instance.project.catalog).endswith("mardmo-model-basics-catalog"):
            config_map = get_uri_prefix_map_model()
        elif str(instance.project.catalog).endswith("mardmo-interdisciplinary-workflow-catalog"):
            config_map = get_uri_prefix_map_workflow()
        elif str(instance.project.catalog).endswith("mardmo-algorithm-catalog"):
            config_map = get_uri_prefix_map_algorithm()
        else:
            return

        # Stop if no Text
        if not instance.text:
            return

        # Get item, config and data information
        label, description, source = extract_parts(instance.text)
        config = config_map[instance.attribute.uri]
        datas = [Relatant.from_triple(instance.external_id, label, description)]

        # Add items from specific source
        if source in ('mardi', 'mathalgodb', 'wikidata'):
            add_entities(
                project=instance.project,
                question_set=config["question_set"],
                datas=datas,
                source=source,
                prefix=config["prefix"]
            )

        # Add items from user
        elif source == 'user':
            add_new_entities(
                project=instance.project,
                question_set=config["question_set"],
                datas=datas,
                prefix=config["prefix"]
            )
