import pytest

from frontend.models import Source


@pytest.mark.django_db
def test_create_source():
    source = Source.objects.create(name="Source")

    assert source.name == "Source"
