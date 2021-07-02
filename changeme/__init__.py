import logging
import os

from flask import Flask, jsonify
from flask_login import LoginManager
from typing import Optional
# from flask_wtf.csrf import CSRFProtect
# from memory_profiler import profile
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

from changeme.conf import Config
from changeme.db import SQL

# csrf = CSRFProtect()
# int_time = Histogram('tfidf_in_seconds', 'Description of histogram')

db = SQL()

_LOG_LEVEl = os.getenv("CHANGEME_LOG", "INFO")
_level = getattr(logging, _LOG_LEVEl)

logging.basicConfig(format='%(asctime)s %(message)s', level=_level)


def create_app(cfg: Optional[Config] = None):
    # pylint: disable=no-member
    # pylint: disable=import-outside-toplevel
    # pylint: disable=relative-beyond-top-level
    if cfg is None:
        cfg = Config()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = cfg.SECRET_KEY

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.INFO)

    # Plugins
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    metrics = GunicornPrometheusMetrics(app)
    metrics.info("app_info", "Application info", version="1.0.3")
    # csrf.init_app(app)

    # ROUTES
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .root import root
    app.register_blueprint(root)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.flask.query(User)\
                       .filter_by(id=int(user_id)).first()
    # prefix = app.config.get('URL_PREFIX', '/api/v1/')
    # from . import documents
    # app.register_blueprint(documents.bp, url_prefix=prefix)

    # errors handlers
    @app.errorhandler(404)
    def server_error(e):
        return jsonify(error=404, text=str(e)), 404

    @app.errorhandler(500)
    def page_not_found(e):
        return jsonify(error=500, text=str(e)), 500

    # @app.after_request
    # def after_request_func(data):
    #     response = app.make_response(data)
    #     response.headers['Content-Type'] = 'application/json; charset=utf8'
    #     return response
    return app
