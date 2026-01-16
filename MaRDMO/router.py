'''Module routing all post_save and post_delete handlers.'''

from django.db.models.signals import post_save
from django.dispatch import receiver
from rdmo.projects.models import Value
from .builders import build_handler_map

HANDLER_MAP = build_handler_map()

@receiver(post_save, sender=Value)
def mardmo_router(sender, instance, update_fields=None, **kwargs):
    """Global post_save router for MaRDMO plugin: dispatch Value saves 
       to correct handler."""

    if not instance:
        return

    catalog = getattr(instance.project, "catalog", None)
    if not catalog or not str(catalog).endswith(
        ("mardmo-model-catalog",
         "mardmo-model-basics-catalog",
         "mardmo-algorithm-catalog",
         "mardmo-interdisciplinary-workflow-catalog")
    ):
        return

    attr_uri = getattr(instance.attribute, "uri", None)
    if not attr_uri:
        return

    catalog_name = str(catalog).rsplit("/", maxsplit = 1)[-1]

    handler = HANDLER_MAP.get(catalog_name, {}).get(attr_uri)
    if handler:
        handler(instance)
