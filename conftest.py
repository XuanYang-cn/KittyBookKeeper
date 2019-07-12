import logging
import pytest
from kitty import create_app, db

logger = logging.getLogger(__name__)


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


def pytest_addoption(parser):
    parser.addoption(
            "--keepdb", action="store", default="true", help="my option: true or false"
            )

@pytest.fixture
def app(request):
    app = create_app('kitty.settings.TestConfig')
    cxt = app.test_request_context()
    cxt.push()

    if request.config.getoption("--keepdb") == 'false':
        db.drop_all()
        db.create_all()
    else:
        db.create_all()

    yield app

    cxt.pop()

    with app.test_request_context():
        if request.config.getoption("--keepdb") == 'false':
            db.drop_all()
        else:
            clear_data(db.session)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_client_runner()
