import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    pass


@pytest.fixture
def no_rollback(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)
