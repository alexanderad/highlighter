import httplib
import requests

from .. import app, request
from ..misc import hashies


@app.route('/v1/parse', method='GET')
def parse():
    url = request.params.get('url')
    if url is None:
        return {'success': False, 'error': 'no url given'}

    url_hash = hashies.md5(url)
    key = 'pages:{}:page_id'.format(url_hash)
    page_id = app.redis.get(key)
    if page_id:
        return {'success': True, 'page_id': page_id, 'cache': 'hit'}

    response = requests.get(
        app.config['mercury.parser_endpoint'],
        params=dict(url=url),
        headers={'x-api-key': app.config['mercury.api_key']}
    )

    if response.status_code != httplib.OK:
        return {'success': False, 'error': response}

    page_id, data = hashies.short_id(), response.json()

    # counters
    app.redis.incr('counters:requests:parse')

    # data
    app.redis.set(key, page_id)
    app.redis.set('pages:{}:url'.format(page_id), url)
    app.redis.set('pages:{}:title'.format(page_id), data['title'])
    app.redis.set('pages:{}:content'.format(page_id), data['content'])
    app.redis.set('pages:{}:image'.format(page_id), data['lead_image_url'])
    app.redis.set('pages:{}:domain'.format(page_id), data['domain'])
    app.redis.set('pages:{}:next_page_url'.format(page_id), data['next_page_url'])
    app.redis.lpush('pages:recent', page_id)

    return {'success': True, 'page_id': page_id, 'cache': 'miss'}
