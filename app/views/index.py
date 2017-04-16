from .. import app, template, request


@app.route('/')
def index():
    return template('index')
