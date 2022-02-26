import requests
from requests.auth import AuthBase


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self._token = token

    def __call__(self, r):
        r.headers["Authorization"] = f'Bearer {self._token}'
        r.headers["Accept"] = "application/json"
        return r


class OAuthToken(requests.auth.AuthBase):
    def __init__(self, oauth_token):
        self.oauth_token = oauth_token

    def __call__(self, r):
        r.headers["OAUTH-TOKEN"] = self.oauth_token
        return r


class ApiKeyAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self._token = token

    def __call__(self, r):
        r.headers["Authorization"] = f'ApiKey {self._token}'
        return r
