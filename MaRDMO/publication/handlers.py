from django.dispatch import receiver
from django.db.models.signals import post_save

from rdmo.projects.models import Value
from rdmo.options.models import Option

from ..config import BASE_URI, mardi_endpoint, mathalgodb_endpoint, mathmoddb_endpoint, wikidata_endpoint, wdt, wd
from ..utils import get_data, get_questionsPU, query_sparql, value_editor
from ..id import *

from .utils import generate_label
from .sparql import queryPublication
from .models import Publication

@receiver(post_save, sender=Value)
def PInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Get Questions of Publication Section
    questions = get_questionsPU()
    # Check if Publication is concerned
    if instance and instance.attribute.uri == f'{BASE_URI}{questions["Publication ID"]["uri"]}':
        # Check if actual Publication selected
        if instance.text and instance.text != 'not found':
            # Get RDMO Options
            options = get_data('data/options.json')
            # Get Source and ID of selected Publication 
            source, id = instance.external_id.split(':')
            # If Publication from MathModDB...
            if source == 'mathmoddb':
                #...query Math MathModDB,...
                query = queryPublication['PublicationMathModDB'].format(id)
                results = query_sparql(query,mathmoddb_endpoint)
                if results:
                    #...structure the data,... 
                    data = Publication.from_query(results)
                    #...and add the Information to the Questionnaire.
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                 text = data.label, 
                                 set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Description"]["uri"]}', 
                                 text = data.description, 
                                 set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Reference"]["uri"]}', 
                                 text = data.doi, 
                                 option = Option.objects.get(uri=options['DOI']), 
                                 collection_index = 0, 
                                 set_index = instance.set_index)
            # If Publication from MathAlgoDB...
            elif source == 'mathalgodb':
                #...query the MathAlgoDB,...
                query = queryPublication['PublicationMathAlgoDB'].format(id)
                results = query_sparql(query,mathalgodb_endpoint)
                if results:
                    #...structure the data...
                    data = Publication.from_query(results)
                    #...and add the Information to the Questionnaire.
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                 text = data.label, 
                                 set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Description"]["uri"]}', 
                                 text = data.description, 
                                 set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Reference"]["uri"]}', 
                                 text = data.doi, 
                                 option = Option.objects.get(uri=options['DOI']), 
                                 collection_index = 0, 
                                 set_index = instance.set_index)
            # If Publication from MaRDI Portal...
            elif source == 'mardi':
                #...query the MaRDI Portal,...
                query = queryPublication['All_MaRDILabel'].format(P16, id, P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23, wdt, wd)
                results = query_sparql(query,mardi_endpoint)
                if results:
                    #...structure the data...
                    data = Publication.from_query(results)
                    #...and add the Information to the Questionnaire.
                    if str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog' or str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                     text = generate_label(data), 
                                     set_index = instance.set_index)
                    else:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                     text = data.label, 
                                     set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Description"]["uri"]}', 
                                 text = data.description, 
                                 set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Reference"]["uri"]}', 
                                 text = data.doi, 
                                 option = Option.objects.get(uri=options['DOI']), 
                                 collection_index = 0, 
                                 set_index = instance.set_index)
            # If Publication from Wikidata...   
            elif source == 'wikidata':
                print('HI')
                #...query Wikidata,...
                query = queryPublication['All_WikidataLabel'].format('356', id, '50', '496', '31', '1433', '407', '1476', '2093', '577', '478', '433', '304', '', '1556')
                print(query)
                results = query_sparql(query,wikidata_endpoint)
                print(results)
                if results:
                    #...structure the data...
                    data = Publication.from_query(results)
                    #and add the Information to the Questionnaire.
                    if str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog' or str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                     text = generate_label(data), 
                                     set_index = instance.set_index)
                    else:
                        value_editor(project = instance.project, 
                                     uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                     text = data.label, 
                                     set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Description"]["uri"]}', 
                                 text = data.description, 
                                 set_index = instance.set_index)
                    value_editor(project = instance.project, 
                                 uri = f'{BASE_URI}{questions["Publication Reference"]["uri"]}', 
                                 text = data.doi, 
                                 option = Option.objects.get(uri=options['DOI']), 
                                 collection_index = 0, 
                                 set_index = instance.set_index)
            # For Models add Relations          
            if str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
                if source == 'mathmoddb':
                    mathmoddb = get_data('model/data/mapping.json')
                    idx = 0
                    for property in ['documents', 'invents', 'studies', 'surveys', 'uses']:
                        if results[0].get(property, {}).get('value'):
                            entities = results[0][property]['value'].split(' / ')
                            for entity in entities:
                                id, label, description = entity.split(' | ')
                                if id and label and description:
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Publication P2E"]["uri"]}', 
                                                 option = Option.objects.get(uri=mathmoddb[property]), 
                                                 set_index = idx, 
                                                 set_prefix = instance.set_index)
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Publication EntityRelatant"]["uri"]}', 
                                                 text = f"{label} ({description}) [mathmoddb]", 
                                                 external_id = id, 
                                                 set_index = idx, 
                                                 set_prefix = instance.set_index)
                                    idx += 1
            # For Algorithms add Relations
            if str(instance.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
                if source == 'mathalgodb':
                    mathalgodb = get_data('algorithm/data/mapping.json')
                    idx = 0
                    for property in ['analyzes', 'applies', 'invents', 'studies', 'surveys']:
                        if results[0].get(property, {}).get('value'):
                            entities = results[0][property]['value'].split(' / ')
                            for entity in entities:
                                id, label, description = entity.split(' | ')
                                if id and label and description:
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Publication P2A"]["uri"]}', 
                                                 option = Option.objects.get(uri=mathalgodb[property]), 
                                                 set_index = idx, 
                                                 set_prefix = instance.set_index)
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Publication ARelatant"]["uri"]}', 
                                                 text = f"{label} ({description}) [mathalgodb]", 
                                                 external_id = id, 
                                                 set_index = idx, 
                                                 set_prefix = instance.set_index)
                                    idx += 1

                    idx = 0
                    for property in ['documents', 'uses']:
                        if results[0].get(property, {}).get('value'):
                            entities = results[0][property]['value'].split(' / ')
                            for entity in entities:
                                id, label, description = entity.split(' | ')
                                if id and label and description:
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Publication P2BS"]["uri"]}', 
                                                 option = Option.objects.get(uri=mathalgodb[property]), 
                                                 set_index = idx, 
                                                 set_prefix = instance.set_index)
                                    value_editor(project = instance.project, 
                                                 uri = f'{BASE_URI}{questions["Publication BSRelatant"]["uri"]}', 
                                                 text = f"{label} ({description}) [mathalgodb]", 
                                                 external_id = id, 
                                                 set_index = idx, 
                                                 set_prefix = instance.set_index)
                                    idx += 1


    return