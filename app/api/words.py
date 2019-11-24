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

    def pick_one(self, redis, installation_id):
        word = random.choice(self._db['words'])
        if any([word.get('is_full_match'), word.get('is_nsfw')]):
            return self.pick_one(redis, installation_id)

        word_key = 'counters:words:{}'.format(word['word'])
        redis.incr(word_key)
        word['seen_times'] = redis.get(word_key) or 0

        return word


words_db = Words()


@app.route('/v1/words/random', method='POST')
def random_word():
    installation_id = request.params.get('installationID', '')
    word = words_db.pick_one(app.redis, installation_id)
    return {'success': True, 'data': word}
