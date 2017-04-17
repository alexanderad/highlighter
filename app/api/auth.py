from requests_oauthlib import OAuth2Session

from app import app, request
from app.ext import decorators
from app.models import User
from app.schemas import AuthTokenSchema


@app.route('/v1/auth/url')
def get_authorization_url():
    """Forms provider authorization URL."""
    google = OAuth2Session(
        app.config['auth.client_id'],
        scope=app.config['auth.scope'],
        redirect_uri=app.config['auth.redirect_uri'])
    authorization_url, state = google.authorization_url(
        app.config['auth.authorization_base_url'],
        access_type='offline', approval_prompt='force')

    # state is used to prevent CSRF, keep this for later
    request.session['oauth_state'] = state

    return {'authorization_url': authorization_url}


@app.post('/v1/auth/token')
@decorators.validate(AuthTokenSchema)
def auth_callback():
    """Retrieves token based on provider callback payload."""
    provider = OAuth2Session(
        app.config['auth.client_id'],
        redirect_uri=app.config['auth.redirect_uri'],
        state=request.session.get('oauth_state'))

    token = provider.fetch_token(
        app.config['auth.token_url'],
        client_secret=app.config['auth.client_secret'],
        authorization_response=request.data.get('callback_url'))

    request.session['oauth_token'] = token

    provider = OAuth2Session(app.config['auth.client_id'], token=token)
    profile = provider.get(app.config['auth.user_info_url']).json()
    user = User.authenticate(profile, token)

    return UserSchema().dump(user).data
