import json
from datetime import timedelta, datetime

import jwt
import requests
from jwt.algorithms import RSAAlgorithm

from config import settings


class AppleOAuth:
    ACCESS_TOKEN_URL = 'https://appleid.apple.com/auth/token'
    KEY_URL = 'https://appleid.apple.com/auth/keys'

    @classmethod
    def apple_login(cls, code):
        client_id, client_secret = AppleOAuth.get_key_and_secret()

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }

        res = requests.post(AppleOAuth.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_data = res.json()
        id_token = res.json().get('id_token', None)

        if id_token:
            decoded = AppleOAuth.parse_id_token(id_token)
            response_data['id_token'] = decoded['sub'] if 'sub' in decoded else None

        return response_data

    @classmethod
    def validate(cls, token):
        client_id, client_secret = AppleOAuth.get_key_and_secret()

        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': token,
            'grant_type': 'refresh_token'
        }

        res = requests.post(AppleOAuth.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_data = res.json()
        id_token = res.json().get('id_token', None)

        if id_token:
            decoded = AppleOAuth.parse_id_token(id_token)
            response_data['id_token'] = decoded['sub'] if 'sub' in decoded else None

        return response_data

    @classmethod
    def get_key_and_secret(cls):
        headers = {
            'kid': settings.SOCIAL_AUTH_APPLE_KEY_ID
        }

        payload = {
            'iss': settings.SOCIAL_AUTH_APPLE_TEAM_ID,
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': settings.CLIENT_ID
        }

        client_secret = jwt.encode(
            payload,
            settings.SOCIAL_AUTH_APPLE_PRIVATE_KEY,
            algorithm='ES256',
            headers=headers
        )

        return settings.CLIENT_ID, client_secret

    @classmethod
    def parse_id_token(cls, id_token):
        kid = jwt.get_unverified_header(id_token).get('kid')

        keys = requests.get(AppleOAuth.KEY_URL).json().get('keys')
        key = list(filter(lambda x: x.get('kid') == kid, keys))[0]
        public_key = RSAAlgorithm.from_jwk(json.dumps(key))

        return jwt.decode(
            id_token,
            key=public_key,
            audience=settings.CLIENT_ID,
            algorithms=['RS256']
        )
