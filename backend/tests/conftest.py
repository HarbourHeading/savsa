import pytest
import mongomock

from ..src.application import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    client = mongomock.MongoClient('localhost', 27017)
    database = client['test']

    yield app

    client.drop_database(database)
    client.close()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
