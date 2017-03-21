from .. import app, template


@app.route('/')
def index():
    return template('index')


@app.route('/debug-redis')
def debug_redis():
    return app.redis.info()
