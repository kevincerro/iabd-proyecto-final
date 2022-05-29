import os
import requests
from flask import request, json
from oauthlib.oauth2 import WebApplicationClient

# Constants
GOOGLE_ID = os.environ.get("GOOGLE_ID")
GOOGLE_SECRET = os.environ.get("GOOGLE_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Google web client
client = WebApplicationClient(GOOGLE_ID)


def init(app):
    if app.debug:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def login():
    google_config = get_google_config()
    endpoint = google_config['authorization_endpoint']

    return client.prepare_request_uri(
        endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )


def callback(code):
    google_config = get_google_config()
    endpoint = google_config['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_ID, GOOGLE_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_config['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    response = userinfo_response.json()
    if response.get('email_verified'):
        return response
    else:
        raise Exception('LoginException', 'User email not available or not verified by Google.')


def get_google_config():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
