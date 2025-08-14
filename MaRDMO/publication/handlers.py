from django.dispatch import receiver
from django.db.models.signals import post_save

from rdmo.projects.models import Value
from rdmo.options.models import Option

from ..config import BASE_URI, endpoint
from ..getters import get_items, get_mathmoddb, get_mathalgodb, get_properties, get_questions_publication
from ..helpers import value_editor
from ..queries import query_sparql
from ..adders import add_basics, add_references, add_relations

from .constants import INDEX_COUNTERS, PROPS, RELATANT_URIS, RELATION_URIS
from .utils import generate_label
from .sparql import queryPublication
from .models import Publication

@receiver(post_save, sender=Value)
def PInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Publication Section
    questions = get_questions_publication()
    # Check if Publication is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Publication"]["ID"]["uri"]}':
        # Check if actual Publication selected
        if instance.text and instance.text != 'not found':
            # Get Source and ID of selected Publication 
            source, id = instance.external_id.split(':')
            # Empty Data as Fallback
            data = {}
            # If Publication from MathAlgoDB...
            if source == 'mathalgodb':
                #...query the MathAlgoDB,...
                query = queryPublication['PublicationMathAlgoDB'].format(id)
                results = query_sparql(query, endpoint['mathalgodb']['sparql'])
                if results:
                    #...structure the data...
                    data = Publication.from_query(results)
                    #...and add the Information to the Questionnaire.
                    add_basics(project = instance.project,
                               text = instance.text,
                               questions = questions,
                               item_type = 'Publication',
                               index = (instance.set_index, None)
                               )
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Publication"]["Reference"]["uri"]}',
                                   set_index = instance.set_index)
            # If Publication from MaRDI Portal...
            elif source == 'mardi':
                #...query the MaRDI Portal,...
                query = queryPublication['MaRDI']['QID_FULL'].format(id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint['mardi']['sparql'])
                if results:
                    #...structure the data...
                    data = Publication.from_query(results)
                    #...and add the Information to the Questionnaire.
                    if str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication"]["Name"]["uri"]}', 
                                     text = generate_label(data), 
                                     set_index = instance.set_index)
                    else:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication"]["Name"]["uri"]}', 
                                     text = data.label, 
                                     set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication"]["Description"]["uri"]}', 
                                 text = data.description, 
                                 set_index = instance.set_index)
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Publication"]["Reference"]["uri"]}',
                                   set_index = instance.set_index)
            # If Publication from Wikidata...   
            elif source == 'wikidata':
                #...query Wikidata,...
                query = queryPublication['Wikidata']['QID_FULL'].format(id)
                results = query_sparql(query, endpoint['wikidata']['sparql-scholarly'])
                if results:
                    #...structure the data...
                    data = Publication.from_query(results)
                    #and add the Information to the Questionnaire.
                    if str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication"]["Name"]["uri"]}', 
                                     text = generate_label(data), 
                                     set_index = instance.set_index)
                    else:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication"]["Name"]["uri"]}', 
                                     text = data.label, 
                                     set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication"]["Description"]["uri"]}', 
                                 text = data.description, 
                                 set_index = instance.set_index)
                    add_references(project = instance.project,
                                   data = data,
                                   uri = f'{BASE_URI}{questions["Publication"]["Reference"]["uri"]}',
                                   set_index = instance.set_index)
            if data:
                # For Models add Relations          
                if str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
                    if source == 'mardi':
                        mathmoddb = get_mathmoddb()
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['P2E'], 
                                      mapping = mathmoddb, 
                                      set_prefix = instance.set_index, 
                                      relatant = f'{BASE_URI}{questions["Publication"]["EntityRelatant"]["uri"]}', 
                                      relation = f'{BASE_URI}{questions["Publication"]["P2E"]["uri"]}')

                # For Algorithms add Relations
                if str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
                    if source == 'mathalgodb':
                        mathalgodb = get_mathalgodb()
                        add_relations(project = instance.project, 
                                      data = data, 
                                      props = PROPS['P2A'], 
                                      mapping = mathalgodb, 
                                      set_prefix = instance.set_index, 
                                      relatant = f'{BASE_URI}{questions["Publication"]["ARelatant"]["uri"]}', 
                                      relation = f'{BASE_URI}{questions["Publication"]["P2A"]["uri"]}')

                        for prop in PROPS['P2BS']:
                            for value in getattr(data, prop):
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions[RELATION_URIS[value.bsclass]]["uri"]}', 
                                             option = Option.objects.get(uri=mathalgodb[prop]), 
                                             set_index = INDEX_COUNTERS[value.bsclass], 
                                             set_prefix = instance.set_index)
                                value_editor(project = instance.project, 
                                             uri = f'{BASE_URI}{questions[RELATANT_URIS[value.bsclass]]["uri"]}', 
                                             text = f"{value.label} ({value.description}) [mathalgodb]", 
                                             external_id = value.id, 
                                             set_index = INDEX_COUNTERS[value.bsclass], 
                                             set_prefix = instance.set_index)
                                INDEX_COUNTERS[value.bsclass] += 1
    return
