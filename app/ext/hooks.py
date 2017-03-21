from .. import app, request


@app.hook('before_request')
def set_session():
    """Handy session shortcut."""
    request.session = request.environ.get('beaker.session')


@app.hook('before_request')
def strip_path():
    """That's a bottle trick."""
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
