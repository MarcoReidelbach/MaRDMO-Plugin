'''MaRDMO Application File'''

from django.apps import AppConfig

class MaRDMOConfig(AppConfig):
    '''MaRDMO Configuration'''

    name = 'MaRDMO'
    label = 'MaRDMO'
    verbose_name = 'MaRDMO Plugin'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.questions = None
        self.mathmoddb = None
        self.mathalgodb = None
        self.options = None
        self.items = None
        self.properties = None

    def ready(self):

        from .getters import get_data

        self.questions = {
            'algorithm': get_data('algorithm/data/questions.json'),
            'model': get_data('model/data/questions.json'),
            'publication': get_data('publication/data/questions.json'),
            'workflow': get_data('workflow/data/questions.json'),
            'search': get_data('search/data/questions.json'),
        }
        self.mathmoddb = get_data('model/data/mapping.json')
        self.mathalgodb = get_data('algorithm/data/mapping.json')
        self.options = get_data('data/options.json')
        self.items = get_data('data/items.json')
        self.properties = get_data('data/properties.json')

        from . import router
