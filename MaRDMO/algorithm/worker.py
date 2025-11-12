'''Worker Module to collect Algorithm Metadata'''

from .constants import PREVIEW_RELATIONS

from ..helpers import entity_relations

def algorithm_relations(answers):
    '''Function to establish relations between Algorithm Documentation Data'''

    # Prepare Relations for Preview
    for relation in PREVIEW_RELATIONS:
        entity_relations(
            data = answers,
            idx = {
                'from': relation[0],
                'to': relation[1]
            },
            entity = {
                'relation': relation[2],
                'old_name': relation[3],
                'new_name': relation[4],
                'encryption': relation[5]
            },
            order = {
                'formulation': False,
                'task': False
            }
        )

    return answers
