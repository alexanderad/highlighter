import functools

from bottle import request, HTTPResponse


def auth_required(callback):
    """Validates authorization."""
    @functools.wraps(callback)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization') or ''
        token = auth_header.replace('Bearer ', '')
        request.user = User.filter(User.access_token == token).first()
        if not request.user:
            return HTTPResponse({'error': 'Unauthorized'}, 401)
        return callback(*args, **kwargs)
    return wrapped


def validate(schema):
    """Validates request against predefined schema."""
    def wrapper(callback):
        @functools.wraps(callback)
        def wrapped(*args, **kwargs):
            data, errors = schema().load(request.json or {})
            if errors:
                return HTTPResponse({'error': errors}, 400)
            request.data = data
            return callback(*args, **kwargs)
        return wrapped
    return wrapper
