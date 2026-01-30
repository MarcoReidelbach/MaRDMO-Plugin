'''Module containing Handlers for the Publication Documentation'''

from django.dispatch import receiver
from django.db.models.signals import post_delete

from rdmo.projects.models import Value
from rdmo.options.models import Option

from ..constants import BASE_URI
from ..getters import (
    get_items,
    get_mathmoddb,
    get_mathalgodb,
    get_properties,
    get_questions,
    get_sparql_query,
    get_url
)
from ..helpers import value_editor
from ..queries import query_sparql
from ..adders import add_basics, add_references, add_relations_flexible

from .constants import (
    INDEX_COUNTERS,
    PROPS,
    RELATANT_URIS,
    RELATION_URIS,
    ITEMINFOS,
    CITATIONINFOS,
    LANGUAGES,
    JOURNALS,
    AUTHORS
)
from .utils import clean_background_data, generate_label
from .models import Publication

class Information:
    '''Class containing functions, querying external sources for specific
       entities and integrating the related metadata into the questionnaire.'''

    def __init__(self):
        '''Load shared data once'''
        self.questions = get_questions('publication')
        self.mathalgodb = get_mathalgodb()
        self.mathmoddb = get_mathmoddb()
        self.base = BASE_URI

    def citation(self, instance):
        '''Citation Information'''

        # Publication specific Questions.
        publication = self.questions["Publication"]

        clean_background_data(
            key_dict = ITEMINFOS | CITATIONINFOS | LANGUAGES | JOURNALS | AUTHORS,
            questions = publication,
            project = instance.project,
            snapshot = instance.snapshot,
            set_index = instance.set_index
        )

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Get Source and ID of selected Publication
        source, identifier = instance.external_id.split(':')

        # Empty Data as Fallback
        data = {}

        # If Publication from MathAlgoDB...
        if source == 'mathalgodb':
            #...query the MathAlgoDB,...
            query = get_sparql_query(
                'publication/queries/doi_from_mathalgodb.sparql'
            ).format(
                identifier
            )
            results = query_sparql(
                query,
                get_url(
                    'mathalgodb',
                    'sparql'
                )
            )

            if not results:
                return

            #...structure the data...
            data = Publication.from_query(results)

            #...and add the Information to the Questionnaire.
            add_basics(
                project = instance.project,
                text = instance.text,
                questions = self.questions,
                item_type = 'Publication',
                index = (instance.set_index, None)
            )

            add_references(
                project = instance.project,
                data = data,
                uri = f'{BASE_URI}{publication["Reference"]["uri"]}',
                set_index = instance.set_index
            )

        # If Publication from MaRDI Portal...
        elif source == 'mardi':
            #...query the MaRDI Portal,...
            query = get_sparql_query(
                'publication/queries/doi_from_mardi.sparql'
            ).format(
                identifier,
                **get_items(),
                **get_properties()
            )

            results = query_sparql(
                query,
                get_url(
                    'mardi',
                    'sparql'
                )
            )

            if not results:
                return

            #...structure the data...
            data = Publication.from_query(results)

            #...and add the Information to the Questionnaire.
            if str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
                value_editor(
                    project = instance.project,
                    uri = f'{BASE_URI}{publication["Name"]["uri"]}',
                    info = {
                        'text': generate_label(data), 
                        'set_index': instance.set_index
                    }
                )
            else:
                value_editor(
                    project = instance.project,
                    uri = f'{BASE_URI}{publication["Name"]["uri"]}',
                    info = {
                        'text': data.label, 
                        'set_index': instance.set_index
                    }
                )

            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{publication["Description"]["uri"]}',
                info = {
                    'text': data.description, 
                    'set_index': instance.set_index
                }
            )

            add_references(
                project = instance.project,
                data = data,
                uri = f'{BASE_URI}{publication["Reference"]["uri"]}',
                set_index = instance.set_index
            )

        # If Publication from Wikidata...
        elif source == 'wikidata':
            #...query Wikidata,...
            query = get_sparql_query(
                'publication/queries/doi_from_wikidata.sparql'
            ).format(
                identifier
            )
            results = query_sparql(
                query,
                get_url(
                    'wikidata',
                    'sparql'
                )
            )

            if not results:
                return

            #...structure the data...
            data = Publication.from_query(results)
            #and add the Information to the Questionnaire.
            if str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
                value_editor(
                    project = instance.project,
                    uri = f'{BASE_URI}{publication["Name"]["uri"]}',
                    info = {
                        'text': generate_label(data), 
                        'set_index': instance.set_index
                    }
                )
            else:
                value_editor(
                    project = instance.project,
                    uri = f'{BASE_URI}{publication["Name"]["uri"]}',
                    info = {
                        'text': data.label, 
                        'set_index': instance.set_index
                    }
                )

            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{publication["Description"]["uri"]}',
                info = {
                    'text': data.description, 
                    'set_index': instance.set_index
                }
            )

            add_references(
                project = instance.project,
                data = data,
                uri = f'{BASE_URI}{publication["Reference"]["uri"]}',
                set_index = instance.set_index
            )

        if data:

            # For Models add Relations
            if str(instance.project.catalog).endswith(
                (
                    'mardmo-model-catalog',
                    'mardmo-model-basics-catalog'
                )
            ):
                if source == 'mardi':
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['P2E'],
                            'mapping': self.mathmoddb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{publication["P2E"]["uri"]}',
                            'relatant': f'{BASE_URI}{publication["EntityRelatant"]["uri"]}',
                        },
                    )

            # For Algorithms add Relations
            if str(instance.project.catalog).endswith('mardmo-algorithm-catalog'):
                if source == 'mathalgodb':
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['P2A'],
                            'mapping': self.mathalgodb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{publication["P2A"]["uri"]}',
                            'relatant': f'{BASE_URI}{publication["ARelatant"]["uri"]}',
                        },
                    )

                    for prop_index, prop in enumerate(PROPS['P2BS']):
                        INDEX_COUNTERS['Benchmark'] = 0
                        INDEX_COUNTERS['Software'] = 0
                        for value in getattr(data, prop):
                            value_editor(
                                project = instance.project,
                                uri = f'{BASE_URI}{publication[RELATION_URIS[value.item_class]]["uri"]}',
                                info = {
                                    'option': Option.objects.get(uri = self.mathalgodb[prop]),
                                    'set_index': prop_index,
                                    'set_prefix': instance.set_index
                                }
                            )
                            value_editor(
                                project = instance.project,
                                uri = f'{BASE_URI}{publication[RELATANT_URIS[value.item_class]]["uri"]}',
                                info = {
                                    'text': f"{value.label} ({value.description}) [mathalgodb]",
                                    'external_id': value.id,
                                    'set_index': prop_index,
                                    'collection_index': INDEX_COUNTERS[value.item_class],
                                    'set_prefix': instance.set_index
                                }
                            )
                            INDEX_COUNTERS[value.item_class] += 1
        return

@receiver(post_delete, sender=Value)
def publication_set_delete(sender, **kwargs):
    '''Handler to delete hidden Publication Information
       upon deletion of Set.
    '''
    instance = kwargs.get("instance", None)
    # Get Questions of Publication Section
    questions = get_questions('publication')
    # Check if Publication is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Publication"]["uri"]}':
        # Loop through "hidden" Data and delete it
        clean_background_data(
            key_dict = ITEMINFOS | CITATIONINFOS | LANGUAGES | JOURNALS | AUTHORS,
            questions = questions["Publication"],
            project = instance.project,
            snapshot = instance.snapshot,
            set_index = instance.set_index
        )
