import httplib
import requests

from app import app, request
from app.misc import hashies
from app.misc.vacuum import VacuumFull


LANGS = {
    'en': 'English',
    'uk': 'Ukrainian',
    'ru': 'Russian',
    'ro': 'Romanian',
    'nl': 'Dutch',
}


def get_dest_langs(source_lang):
    return {
        code: lang
        for code, lang in LANGS.items()
        if code != source_lang
    }


def detect_language(text, try_again=True):
    text = VacuumFull(text).apply_all()[:256]

    response = requests.post(
        '{}/detect?api-version=3.0'.format(app.config['translate.endpoint']),
        json=[{"Text": text}],
        headers={
            'Ocp-Apim-Subscription-Key': app.config['translate.api_key']
        }
    ).json()
    app.redis.incr('counters:requests:detect_language')
    if 'error' not in response:
        return response[0].get('language')

    if try_again:
        return detect_language(text[len(text) / 2: len(text) / 2 + 1024], try_again=False)

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

    response = requests.post(
        '{}/translate?api-version=3.0&from={}&to={}'.format(
            app.config['translate.endpoint'],
            source_lang,
            dest_lang
        ),
        json=[{"Text": text}],
        headers={
            'Ocp-Apim-Subscription-Key': app.config['translate.api_key']
        }
    ).json()

    if 'error' not in response:
        translated = response[0].get('translations')[0].get('text')
    else:
        return {'success': False, 'error': response}

    # counters
    app.redis.incr('counters:requests:translate')
    app.redis.incrby('counters:characters:translated', len(text))

    # data
    app.redis.set(key, translated)
    app.redis.set('text:{}:{}'.format(text_hash, source_lang), text)

    return {'success': True, 'text': translated, 'cache': 'miss'}
