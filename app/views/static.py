import os

from .. import app, static_file


@app.route('/static/<file_path:path>')
def serve_static(file_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    static_path = os.path.join(dir_path, '..', 'static/')
    return static_file(file_path, root=static_path)
