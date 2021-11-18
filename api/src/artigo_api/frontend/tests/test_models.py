import pytest
from django.test import TestCase

from frontend.models import Institution


@pytest.mark.django_db
def test_create_source():
    institution = Institution.objects.create(name="Institution")

    assert institution.name == "Institution"
