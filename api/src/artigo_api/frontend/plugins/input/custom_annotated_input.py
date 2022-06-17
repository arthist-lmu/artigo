import logging

from frontend.plugins import InputPluginManager
from ..taboo.custom_annotated_taboo import CustomAnnotatedTaboo

logger = logging.getLogger(__name__)


@InputPluginManager.export('CustomAnnotatedInput')
class CustomAnnotatedInput(CustomAnnotatedTaboo):
    pass
