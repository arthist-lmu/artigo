from ..database import Backbone


def test_backbone():
    backbone = Backbone(config=None)
    
    assert backbone.status() == 'ok'
