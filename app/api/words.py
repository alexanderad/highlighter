import os.path
import json
import httplib
import requests
import json
import random
import csv

from app import app, request
from app.ext import decorators


class Words():
    def __init__(self):
        self._db = self._load_db(app.config['words.db'])

    def _load_db(self, db_file):
        import app as root
        work_dir = os.path.dirname(root.__file__)
        with open(os.path.join(work_dir, db_file), 'r') as f:
            if db_file.endswith('.json'):
                return json.load(f)

            return {'words': [x for x in csv.DictReader(f)]}

    def pick_one(self):
        return random.choice(self._db['words'])


words_db = Words()


@app.route('/v1/words/random', method='GET')
def random_word():
        word = words_db.pick_one()
    app.redis.incr('counters:words:{}'.format(word['word']))
    return {'success': True, 'data': word}
