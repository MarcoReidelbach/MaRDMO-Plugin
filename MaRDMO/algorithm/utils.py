from ..config import BASE_URI
from ..utils import value_editor

from ..model.utils import get_id

def add_publication(instance, publications, source):
    # Get Set Ids and IDs of Publications
    set_ids = get_id(instance, f'{BASE_URI}domain/publication', ['set_index'])
    value_ids = get_id(instance, f'{BASE_URI}domain/publication/id', ['external_id'])
    # Add Publication to Questionnaire
    idx = max(set_ids, default = -1) + 1
    for publication in publications:
        if publication.id not in value_ids:
            # Set up Page
            value_editor(instance.project, f'{BASE_URI}domain/publication', f"P{idx}", None, None, None, idx)
            # Add ID Values
            value_editor(instance.project, f'{BASE_URI}domain/publication/id', f'{publication.label} ({publication.description}) [{source}]', f"{publication.id}", None, None, idx)
            idx += 1
            value_ids.append(publication.id)
    return