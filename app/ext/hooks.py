from .. import app, request, response


@app.route('/<:re:.*>', method='OPTIONS')
def cors():
    response.headers.update(**app.get_cors_headers())


@app.hook('before_request')
def set_session():
    """Handy session shortcut."""
    request.session = request.environ.get('beaker.session')


@app.hook('before_request')
def strip_path():
    """That's a bottle trick."""
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
