import logging

from frontend.plugins import InputPluginManager
from ..taboo.most_annotated_tagging_taboo import MostAnnotatedTaggingTaboo

logger = logging.getLogger(__name__)


@InputPluginManager.export('MostAnnotatedTaggingInput')
class MostAnnotatedTaggingInput(MostAnnotatedTaggingTaboo):
    pass
