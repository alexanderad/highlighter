from app import app

@app.route('/v1/stats', method='GET')
def stats():
    keys = [
        'counters:requests:index',
        'counters:requests:read',
        'counters:requests:parse',
        'counters:requests:translate',
        'counters:requests:detect_language',
        'counters:characters:translated'
    ]
    return {key: app.redis.get(key) for key in keys}
