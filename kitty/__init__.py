from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from kitty import settings
from restplus_enhancement.namespace import Namespace
from sqlalchemy_enhancement.base_query import BaseQuery


from flask_restplus import Api
api = Api(title=settings.DOC_TITLE,
          version=settings.DOC_VERSION,
          doc=settings.DOC_URL)


db = SQLAlchemy(query_class=BaseQuery)
migrate = Migrate()


def create_app(testing_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = settings.FLASK_STRICT_SLASHES

    app.config.from_object(settings.DefaultConfig)

    if testing_config:
        app.config.from_object(testing_config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()
kitty_api = Namespace("BookKeeper", description='book keeper restful api', path='/', validate=True)

from kitty import views, errorhandlers, errors
from kitty import models


api.add_namespace(kitty_api)
api.init_app(app)
