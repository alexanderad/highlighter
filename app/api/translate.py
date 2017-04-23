import httplib
import requests

from app import app, request
from app.misc import hashies


DESTS = {
    'en': 'English',
    'uk': 'Ukrainian',
    'ru': 'Russian',
    'ro': 'Romanian'
}
ADDITIONAL_DESTS = {
    # 'en': {
    #     'def': 'Definitions'
    # }
}


def get_dest_langs(source_lang):
    dest_langs = {
        code: lang
        for code, lang in DESTS.items()
        if code != source_lang
    }
    dest_langs.update(ADDITIONAL_DESTS.get(source_lang, {}))
    return dest_langs

@app.route('/v1/translate', method='POST')
def translate():
    text = request.params.get('text')
    if not text:
        return {'success': False, 'error': 'no text given'}

    if len(text) > 128:
        return {'success': False, 'error': 'text is too long'}

    # set in stone for now
    source_lang, dest_lang = 'ro', 'en'

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
