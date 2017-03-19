import httplib
import redis
import requests
import bottle
from bottle import Bottle, request, run, template

app = Bottle()
redis = redis.StrictRedis()

API_KEY = 'trnsl.1.1.20170318T185046Z.71fb45e0a4426d74.3da79b5e55569e3c36f8bb68caa94fc8c365ffa6'
MAX_LENGTH = 128


def translate_text(text):
    key = 'translated:text:{}'.format(text)
    translated = redis.get(key)
    if translated:
        return {'success': True, 'text': translated, 'cache': 'hit'}

    if not translated:
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&lang=ro-en&text={}'
        response = requests.get(url.format(API_KEY, text)).json()
        if response.get('code') == httplib.OK:
            translated = response.get('text').pop()

        redis.incr('translated:count')
        redis.incrby('translated:count_characters', len(text))
        redis.setnx('translated:text:{}'.format(text), translated)
        return {'success': True, 'text': translated, 'cache': 'miss'}

    return {'success': False, 'error': response}


@app.route('/')
def index():
    return template('templates/index')


@app.route('/translate')
def translate():
    text = request.params.get('text')
    if text is None:
        return {'success': False, 'error': 'no text given'}

    if len(text) > MAX_LENGTH:
        return {'success': False, 'error': 'text is too long'}

    return translate_text(text)

run(app, host='localhost', port=8080, debug=True, reload=True)
