import pytest

from frontend.cache import (
    resource_count,
    resource_tagging_count,
)


@pytest.mark.django_db
class TestCache:
    def test_resource_count(self):
        values = resource_count(renew=True)

        assert values > 0

    def test_resource_tagging_count(self):
        values = resource_tagging_count(renew=True)

        assert len(values) > 0
