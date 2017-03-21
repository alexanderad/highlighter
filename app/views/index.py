from .. import app, template


@app.route('/')
def index():
    return template('index')
