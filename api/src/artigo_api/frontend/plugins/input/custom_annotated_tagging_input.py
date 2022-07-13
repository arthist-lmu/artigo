import logging

from frontend.plugins import InputPluginManager
from ..taboo.custom_annotated_tagging_taboo import CustomAnnotatedTaggingTaboo

logger = logging.getLogger(__name__)


@InputPluginManager.export('CustomAnnotatedTaggingInput')
class CustomAnnotatedTaggingInput(CustomAnnotatedTaggingTaboo):
    pass
