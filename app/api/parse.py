import httplib
import requests
import subprocess
import json

from app import app, request
from app.misc import hashies
from app.misc.vacuum import Vacuum
from app.api.translate import detect_language


@app.route('/v1/parse', method='POST')
def parse():
    url = request.params.get('url').strip()
    if not url:
        return {
            'success': False,
            'error': 'The url parameter passed does not look like a valid URL.'
        }

    url_hash = hashies.md5(url)
    key = 'pages:{}:page_id'.format(url_hash)
    page_id = app.redis.get(key)
    if page_id:
        return {'success': True, 'page_id': page_id, 'cache': 'hit'}

    try:
        response = subprocess.check_output(["mercury-parser", url])
        data = json.loads(response.strip())
    except Exception as e:
        return {'success': False, 'error': repr(e)}

    if data.get('error'):
        return {'success': False, 'error': data['messages']}

    page_id = hashies.short_id()
    content = data.get('content') or ''
    if not content:
        return {'success': False, 'error': 'Failed to extract page contents'}

    content = Vacuum(content).apply_all()

    # counters
    app.redis.incr('counters:requests:parse')

    # data
    app.redis.set(key, page_id)
    app.redis.lpush('pages:recent', page_id)
    app.redis.set('pages:{}'.format(page_id), url)
    app.redis.set('pages:{}:title'.format(page_id),
                  data.get('title', 'No title'))
    app.redis.set('pages:{}:content'.format(page_id), content)
    app.redis.set('pages:{}:domain'.format(page_id), data.get('domain', ''))
    app.redis.set('pages:{}:lang'.format(page_id), detect_language(content))

    return {'success': True, 'page_id': page_id, 'cache': 'miss'}
