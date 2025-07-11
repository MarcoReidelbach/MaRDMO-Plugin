from django.apps import AppConfig

class MaRDMOConfig(AppConfig):
    name = 'MaRDMO'
    label = 'MaRDMO'
    verbose_name = 'MaRDMO Plugin'

    def ready(self):
        from .getters import get_data
        from .algorithm import handlers
        from .model import handlers
        from .workflow import handlers
        from .publication import handlers

        self.questions_algorithm = get_data('algorithm/data/questions.json')
        self.questions_model = get_data('model/data/questions.json')
        self.questions_publication = get_data('publication/data/questions.json')
        self.questions_workflow = get_data('workflow/data/questions.json')
        self.questions_search = get_data('search/data/questions.json')
        self.mathmoddb = get_data('model/data/mapping.json')
        self.mathalgodb = get_data('algorithm/data/mapping.json')
        self.options = get_data('data/options.json')
        self.ITEMS = get_data('data/items_staging.json')
        self.PROPERTIES = get_data('data/properties_staging.json')
        
        

