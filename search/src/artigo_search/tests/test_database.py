import pytest

from artigo_search.database.backbone import Backbone


def test_backbone():
    backbone = Backbone(config=None)
    
    assert backbone.status() == 'ok'
