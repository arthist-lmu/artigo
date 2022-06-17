import logging

from frontend.plugins import InputPluginManager
from ..taboo.most_annotated_taboo import MostAnnotatedTaboo

logger = logging.getLogger(__name__)


@InputPluginManager.export('MostAnnotatedInput')
class MostAnnotatedInput(MostAnnotatedTaboo):
    pass
