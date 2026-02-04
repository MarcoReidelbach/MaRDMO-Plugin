'''Worker Module for Algorithm Preview and Export'''

from .constants import preview_relations
from ..getters import get_items, get_mathalgodb, get_properties
from ..helpers import entity_relations

class PrepareAlgorithm:
    '''Class preparing Model Answers for Preview and Export'''
    def __init__(self):
        self.mathalgodb = get_mathalgodb()
        self.items = get_items()
        self.properties = get_properties()

    def preview(self, answers):
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
