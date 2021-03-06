import os

from flask import Flask
from flaskext.markdown import Markdown


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Markdown(app)

    # @app.route('/')
    # def index():
    #     return 'Hello world'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.auth)

    from . import blog
    app.register_blueprint(blog.blog)
    app.add_url_rule('/', endpoint='index')

    return app
