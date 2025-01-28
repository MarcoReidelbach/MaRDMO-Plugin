from django.apps import AppConfig

class MaRDMOConfig(AppConfig):
    name = 'MaRDMO'
    label = 'MaRDMO'
    verbose_name = 'MaRDMO Plugin'

    def ready(self):
        from .algorithm import handlers
        from .model import handlers
        from .workflow import handlers
        from .publication import handlers
