import httplib
import requests

from app import app, request
from app.misc import hashies


LANGS = {
    'en': 'English',
    'uk': 'Ukrainian',
    'ro': 'Romanian',
    'nl': 'Dutch',
}


def get_dest_langs(source_lang):
    return {
        code: lang
        for code, lang in LANGS.items()
        if code != source_lang
    }


@app.route('/v1/translate', method='POST')
def translate():
    text = request.params.get('text')
    if not text:
        return {'success': False, 'error': 'no text given'}

    if len(text) > 128:
        return {'success': False, 'error': 'text is too long'}

    source_lang = request.params.get('source_lang')
    dest_lang = request.params.get('dest_lang')

    text_hash = hashies.md5(text)

    key = 'text:{}:{}'.format(text_hash, dest_lang)
    translated = app.redis.get(key)
    if translated:
        return {'success': True, 'text': translated, 'cache': 'hit'}

    response = requests.get(
        '{}/translate'.format(app.config['yandex.endpoint']),
        params=dict(
            key=app.config['yandex.api_key'],
            lang='{}-{}'.format(source_lang, dest_lang),
            text=text
        )
    ).json()

    if response.get('code') == httplib.OK:
        translated = response.get('text').pop()
    else:
        return {'success': False, 'error': response}

    # counters
    app.redis.incr('counters:requests:translate')
    app.redis.incrby('counters:characters:translated', len(text))

    # data
    app.redis.set(key, translated)
    app.redis.set('text:{}:{}'.format(text_hash, source_lang), text)

    return {'success': True, 'text': translated, 'cache': 'miss'}
