import logging

from bottle import run

from app import app


if __name__ == "__main__":
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.WARNING)

    run_args = {
        key.replace('run.', ''): value
        for key, value in app.config.items() if key.startswith('run.')
    }
    run(app, **run_args)
