import json
import httplib
import requests

from app import app, request
from app.ext import decorators
from app.schemas import WordSchema


@app.route('/v1/words', method='POST')
@decorators.validate(WordSchema)
def add_word():
    data = request.data
    app.redis_words.set(
        'words:{}:{}'.format(data['lang'], data['word']), json.dumps(data))
    return {'success': True}


@app.route('/v1/words/random', method='GET')
def random_word():
    key = app.redis_words.randomkey()
    if key is None:
        return {'success': False, 'data': None}

    return {'success': True, 'data': json.loads(app.redis_words.get(key))}
