from app import app, template, request, redirect
from app.api.translate import get_dest_langs


@app.route('/')
def index():
    app.redis.incr('counters:requests:index')

    return template('index')


@app.route('/parse')
def parse():
    app.redis.incr('counters:requests:parse')

    url = request.params.get('u')
    if not url:
        return redirect('/')

    return template('parse')


@app.route('/read')
def read():
    app.redis.incr('counters:requests:read')

    page_id = request.params.get('t')
    if not page_id:
        return redirect('/')

    root_key = 'pages:{}'.format(page_id)
    url = app.redis.get(root_key)
    if not url:
        return redirect('/')

    app.redis.incr('{}:views'.format(root_key))
    context = {
        key: app.redis.get('{}:{}'.format(root_key, key))
        for key in (
            'title', 'domain', 'content', 'next_page_url', 'lang'
        )
    }
    context['page_id'] = page_id
    context['url'] = url
    context['dest_langs'] = get_dest_langs(context['lang'])

    dest_lang = request.params.get('l')
    if not dest_lang or dest_lang not in context['dest_langs']:
        dest_lang = 'en'

    context['dest_lang'] = dest_lang

    return template('read', **context)
