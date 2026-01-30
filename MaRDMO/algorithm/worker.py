'''Worker Module to collect Algorithm Metadata'''

from .constants import preview_relations

from ..helpers import entity_relations

def algorithm_relations(answers):
    '''Function to establish relations between Algorithm Documentation Data'''

    # Prepare Relations for Preview
    for relation in preview_relations:
        entity_relations(
            data = answers,
            idx = {
                'from': relation['from_idx'],
                'to': relation['to_idx']
            },
            entity = {
                'relation': relation['relation'],
                'old_name': relation['old_name'],
                'new_name': relation['new_name'],
                'encryption': relation['encryption']
            },
            order = {
                'formulation': False,
                'task': False
            },
            assumption = False
        )

    return answers
