import logging

from frontend.plugins import InputPluginManager
from ..taboo.random_annotated_taboo import RandomAnnotatedTaboo

logger = logging.getLogger(__name__)


@InputPluginManager.export('RandomAnnotatedInput')
class RandomAnnotatedInput(RandomAnnotatedTaboo):
    pass
