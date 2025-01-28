from django.dispatch import receiver
from django.db.models.signals import post_save

from rdmo.projects.models import Value
from rdmo.options.models import Option

from ..config import BASE_URI, mardi_endpoint, mathalgodb_endpoint, mathmoddb_endpoint, wikidata_endpoint, wdt, wd
from ..utils import get_data, query_sparql, value_editor
from ..id import *

from .utils import generate_label
from .sparql import queryPublication
from .models import Publication

@receiver(post_save, sender=Value)
def PInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/publication/id':
        if instance.text and instance.text != 'not found':
            
            options = get_data('data/options.json')
            source, id = instance.external_id.split(':')
            
            if source == 'mathmoddb':
                query = queryPublication['PublicationMathModDB'].format(f":{id}")
                results = query_sparql(query,mathmoddb_endpoint)
                if results:
                    data = Publication.from_query(results)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/name', data.label, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', data.description, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, instance.set_index)
            
            elif source == 'mathalgodb':
                query = queryPublication['PublicationMathAlgoDB'].format(f"pb:{id}")
                results = query_sparql(query,mathalgodb_endpoint)
                print(results)
                if results:
                    data = Publication.from_query(results)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/name', data.label, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', data.description, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, instance.set_index)
            
            elif source == 'mardi':
                query = queryPublication['All_MaRDILabel'].format(P16, f"wd:{id}", P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23, wdt, wd)
                results = query_sparql(query,mardi_endpoint)
                if results:
                    data = Publication.from_query(results)
                    print(data)
                    if str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', generate_label(data), None, None, None, instance.set_index)
                    else:
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', data.label, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', data.description, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, instance.set_index)
                    
            elif source == 'wikidata':
                query = queryPublication['All_WikidataLabel'].format('356', f"wd:{id}", '50', '496', '31', '1433', '407', '1476', '2093', '577', '478', '433', '304', '', '1556')
                results = query_sparql(query,wikidata_endpoint)
                if results:
                    data = Publication.from_query(results)
                    if str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', generate_label(data), None, None, None, instance.set_index)
                    elif str(instance.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', data.label, None, None, None, instance.set_index)   
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', data.description, None, None, None, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, instance.set_index)
                    
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
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/entity-relation', None, None, Option.objects.get(uri=mathmoddb[property]), None, idx, instance.set_index)
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/entity-relatant', f"{label} ({description}) [mathmoddb]", f'{id}', None, None, idx, instance.set_index)
                                    idx += 1

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
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/algorithm-relation', None, None, Option.objects.get(uri=mathalgodb[property]), None, idx, instance.set_index)
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/algorithm-relatant', f"{label} ({description}) [mathalgodb]", f'{id}', None, None, idx, instance.set_index)
                                    idx += 1

                    idx = 0
                    for property in ['documents', 'uses']:
                        if results[0].get(property, {}).get('value'):
                            entities = results[0][property]['value'].split(' / ')
                            for entity in entities:
                                id, label, description = entity.split(' | ')
                                if id and label and description:
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/benchmark-or-software-relation', None, None, Option.objects.get(uri=mathalgodb[property]), None, idx, instance.set_index)
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/benchmark-or-software-relatant', f"{label} ({description}) [mathalgodb]", f'{id}', None, None, idx, instance.set_index)
                                    idx += 1


    return