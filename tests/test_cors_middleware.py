import pytest
from flask import Flask

from app.middleware.cors_middleware import init_cors


def create_app_with_origins(origins, debug=False):
    app = Flask(__name__)
    app.config['FRONTEND_ORIGINS'] = origins
    app.config['DEBUG'] = debug
    init_cors(app)

    @app.route('/test')
    def test():
        return 'ok'

    return app


def test_echo_origin_allowed():
    origins = 'http://localhost:3000,https://v0-extractedfrontend.vercel.app'
    app = create_app_with_origins(origins)
    client = app.test_client()
    headers = {'Origin': 'https://v0-extractedfrontend.vercel.app'}
    resp = client.get('/test', headers=headers)

    assert resp.status_code == 200
    assert resp.headers.get('Access-Control-Allow-Origin') == 'https://v0-extractedfrontend.vercel.app'


def test_no_echo_origin_not_allowed():
    app = create_app_with_origins('http://localhost:3000')
    client = app.test_client()
    headers = {'Origin': 'https://evil.example.com'}
    resp = client.get('/test', headers=headers)

    assert resp.status_code == 200
    assert 'Access-Control-Allow-Origin' not in resp.headers
