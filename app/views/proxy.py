import requests
from bottle import HTTPResponse

from .. import app, abort, request
from ..misc import hashies


@app.route('/https')
def https():
    url = request.params.get('u')
    signature = request.params.get('s')
    if not any([url, signature]):
        abort(400, 'Bad Request')

    salt = app.config['app.secret']
    if not hashies.validate_string_signature(url, salt, signature):
        abort(400, 'Bad Request')

    response = requests.get(url)

    return HTTPResponse(
        status=response.status_code,
        body=response.content,
        content_type=response.headers['Content-Type']
    )
