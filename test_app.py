import pytest
import json

from solution import app

@pytest.fixture
def application():

    application = app.test_client()
    yield application


def test_decryptEmptyBody(application):
    reply = application.post('/decryptMessage')

    assert'Empty body' == reply.get_json()['error']

def test_invalidBody(application):
    reply = application.post('/decryptMessage', data=json.dumps(dict(z='a', q='b')), content_type='application/json')
    assert 'Invalid Body' == reply.get_json()['error']

def test_invalidMethod(application):
    reply = application.get('/decryptMessage')
    assert 'Method Not Allowed' == reply.get_json()['error']


def test_invalidPassphrase(application):
    message = 'eerer'
    passphrase = 'rggr'

    reply = application.post('/decryptMessage', data=json.dumps(dict(message=str(message), passphrase=passphrase)), content_type='application/json')

    assert'Invalid Passphrase' == reply.get_json()['error']