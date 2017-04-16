import httplib
import shortid
import requests

from .. import app, request


def parse_page(url):
    key = 'parsed:url:{}'.format(url)
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

    page_id = shortid.ShortId().generate()
    data = response.json()

    app.redis.incr('counter:parse_requests')
    app.redis.set('parsed:url:{}'.format(url), page_id)
    app.redis.set('parsed:title:{}'.format(page_id), data['title'])
    app.redis.set('parsed:content:{}'.format(page_id), data['content'])
    app.redis.set('parsed:image:{}'.format(page_id), data['lead_image_url'])
    app.redis.set('parsed:domain:{}'.format(page_id), data['domain'])

    return {'success': True, 'page_id': page_id, 'cache': 'miss'}


@app.route('/v1/parse', method='POST')
def parse():
    url = request.params.get('url')
    if url is None:
        return {'success': False, 'error': 'no url given'}

    return parse_page(url)
