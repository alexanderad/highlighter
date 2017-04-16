import httplib
import requests

from .. import app, request


def translate_text(text):
    key = 'translated:text:{}'.format(text)
    translated = app.redis.get(key)
    if translated:
        return {'success': True, 'text': translated, 'cache': 'hit'}

    response = requests.get(
        app.config['yandex.translate_endpoint'],
        params=dict(
            key=app.config['yandex.api_key'],
            lang='ro-en',
            text=text
        )
    ).json()

    if response.get('code') == httplib.OK:
        translated = response.get('text').pop()
    else:
        return {'success': False, 'error': response}

    app.redis.incr('counter:translate_requests')
    app.redis.incrby('counter:translated_characters', len(text))
    app.redis.setnx('translated:text:{}'.format(text), translated)

    return {'success': True, 'text': translated, 'cache': 'miss'}


@app.route('/v1/translate', method='POST')
def translate():
    text = request.params.get('text')
    if text is None:
        return {'success': False, 'error': 'no text given'}

    if len(text) > 128:
        return {'success': False, 'error': 'text is too long'}

    return translate_text(text)
