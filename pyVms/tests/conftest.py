import pytest

from app.app import app as vm_app


@pytest.fixture
def app():
    yield vm_app


@pytest.fixture
def client(app):
    return app.test_client()
