from .. import app, template, request, redirect


@app.route('/')
def index():
    return template('index')


@app.route('/parse')
def parse():
    url = request.params.get('u')
    if not url:
        return redirect('/')

    return template('parse')


@app.route('/read')
def read():
    page_id = request.params.get('t')
    if not page_id:
        return redirect('/')

    root_key = 'pages:{}'.format(page_id)
    url = app.redis.get(root_key)
    if not url:
        return redirect('/')

    page = {
        key: app.redis.get('{}:{}'.format(root_key, key))
        for key in ('title', 'domain', 'content', 'next_page_url')
    }

    return template('read', url=url, **page)
