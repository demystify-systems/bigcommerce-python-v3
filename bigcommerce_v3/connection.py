# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import time

from bigcommerce_v3 import (
    API_V2_BASIC_AUTH_PATH,
    API_V2_OAUTH_PATH,
    API_V3_BASIC_AUTH_PATH,
    API_V3_OAUTH_PATH
)

import bigcommerce
from bigcommerce.connection import log

import requests


class Connection(bigcommerce.connection.Connection):
    def __init__(self, host, auth, api_path='/api/v2/{}', max_retries=6):
        super(Connection, self).__init__(host, auth, api_path)
        self.auth = auth
        self.max_retries = max_retries

    def full_path(self, url, api_version='v2'):
        if api_version == 'v2':
            path = "https://" + self.host + API_V2_BASIC_AUTH_PATH.format(url)
        else:
            path = "https://" + self.host + API_V3_BASIC_AUTH_PATH.format(url)

        return path

    def _reset_session(self):
        self._session = requests.Session()
        self._session.auth = self.auth
        self._session.headers = {"Accept": "application/json"}


class OAuthConnection(bigcommerce.connection.OAuthConnection):
    def __init__(
        self, client_id, store_hash, access_token=None, host='api.bigcommerce.com',
        api_path='/stores/{}/v2/{}', rate_limiting_management=None, max_retries=6):
        super(OAuthConnection, self).__init__(
            client_id, store_hash, access_token, host, api_path, rate_limiting_management)
        self.access_token = access_token
        self.max_retries = max_retries

    def full_path(self, url, api_version='v2'):
        if api_version == 'v2':
            path = "https://" + self.host + API_V2_OAUTH_PATH.format(self.store_hash, url)
        else:
            path = "https://" + self.host + API_V3_OAUTH_PATH.format(self.store_hash, url)

        return path

    def _handle_response(self, url, res, suppress_empty=True):
        return bigcommerce.connection.OAuthConnection._handle_response(
            self, url, res, suppress_empty)

    def _reset_session(self):
        self._session = requests.Session()
        self._session.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip"
        }
        if self.access_token and self.store_hash:
            self._session.headers.update(self._oauth_headers(self.client_id, self.access_token))
