from .. import app, template, request


@app.route('/')
def index():
    return template('index')


@app.route('/debug-redis')
def debug_redis():
    return app.redis.info()


@app.route('/parser')
def parser():

    import requests

    url = request.params.get('url')



    return template('parser', **response.json())
