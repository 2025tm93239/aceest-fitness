import pytest

from aceest.storage import reset_clients
from app import create_app


@pytest.fixture
def app():
    reset_clients()
    flask_app = create_app(testing=True)
    yield flask_app
    reset_clients()


@pytest.fixture
def client(app):
    return app.test_client()
