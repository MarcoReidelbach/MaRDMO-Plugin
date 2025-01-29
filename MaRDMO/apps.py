from django.apps import AppConfig

class MaRDMOConfig(AppConfig):
    name = 'MaRDMO'
    label = 'MaRDMO'
    verbose_name = 'MaRDMO Plugin'

    def ready(self):
        from .utils import get_data
        from .algorithm import handlers
        from .model import handlers
        from .workflow import handlers
        from .publication import handlers
        
        self.questionsAL = get_data('algorithm/data/questions.json')
        self.questionsPU = get_data('publication/data/questions.json')

