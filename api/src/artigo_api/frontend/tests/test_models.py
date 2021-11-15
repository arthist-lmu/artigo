import pytest

from artigo.api.src.artigo_api.frontend.models import Institution


@pytest.mark.django_db
def test_create_source():
    institution = Institution.objects.create(name="Institution")

    assert institution.name == "Institution"
