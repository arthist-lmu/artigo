import logging

from frontend.plugins import InputPluginManager
from ..taboo.random_annotated_tagging_taboo import RandomAnnotatedTaggingTaboo

logger = logging.getLogger(__name__)


@InputPluginManager.export('RandomAnnotatedTaggingInput')
class RandomAnnotatedTaggingInput(RandomAnnotatedTaggingTaboo):
    pass
