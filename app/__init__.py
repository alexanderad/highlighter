import os

import redis
from bottle import abort, request, response, redirect, template, static_file
from .ext.app import BottleExt


def create_app():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    app = BottleExt()
    app.config.load_config(os.path.join(dir_path, 'app.conf'))
    app.config.load_config(os.path.join(dir_path, 'app.dev.conf'))

    if os.getenv('PRODUCTION'):
        app.config.load_config(os.path.join(dir_path, 'app.prod.conf'))

    if os.getenv('CI'):
        app.config.load_config(os.path.join(dir_path, 'app.ci.conf'))

    app.setup_sessions(app.config)
    app.redis = redis.StrictRedis(
        host=app.config['redis.host'], port=app.config['redis.port'], db=0)
    app.redis_words = redis.StrictRedis(
        host=app.config['redis.host'], port=app.config['redis.port'], db=1)

    return app


app = create_app()
from .ext import hooks
from . import views
from . import api
