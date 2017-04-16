import httplib
import requests

from .. import app, request


def parse_page(url):
    key = 'translated:text:{}'.format(text)
    translated = app.redis.get(key)
    if translated:
        return {'success': True, 'text': translated, 'cache': 'hit'}

    response = requests.get(
        app.config['mercury.parser_endpoint'],
        params=dict(url=url),
        headers={'x-api-key': app.config['mercury.api_key']}
    )

    if response.get('code') == httplib.OK:
        translated = response.get('text').pop()
    else:
        return {'success': False, 'error': response}

    app.redis.incr('counter:translate_requests')
    app.redis.incrby('counter:translated_characters', len(text))
    app.redis.setnx('translated:text:{}'.format(text), translated)

    return {'success': True, 'text': translated, 'cache': 'miss'}


@app.route('/v1/parse', method='POST')
def parse():
    url = request.params.get('url')
    if url is None:
        return {'success': False, 'error': 'no url given'}

    page = parse_page(url)

    return redi
