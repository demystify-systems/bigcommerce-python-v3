# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import json
import time

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from bigcommerce.resources.base import ApiResource
from bigcommerce.connection import Connection
from bigcommerce.connection import log
from bigcommerce.exception import ServerException, RateLimitingException
from wrapt import apply_patch
from requests.exceptions import (ConnectTimeout, ConnectionError, ReadTimeout)


@classmethod
def _make_request(cls, method, url, connection, data=None, params=None, headers=None):
    result = None

    api_version = getattr(cls, 'api_version') if hasattr(cls, 'api_version') else 'v2'
    retries = connection.max_retries
    while retries > 0:
        try:
            result = connection.make_request(
                method, url, data, params, headers, api_version=api_version)
            if isinstance(result, dict) and 'data' in result:
                result = result['data']

            break
        except ServerException:
            log.exception(e)
            retries -= 1
            log.info('[RetryServerException] Retry remaining: %d', retries)
        except RateLimitingException as e:
            log.exception(e)
            time.sleep(3)
            log.info('[RetryRateLimitingException] Retry remaining: %d', retries)

    return result

def make_request(self, method, url, data=None, params=None, headers=None, api_version='v2'):
    response = self._run_method(method, url, data, params, headers, api_version)
    return self._handle_response(url, response)

def _run_method(self, method, url, data=None, query=None, headers=None, api_version='v2'):
    if query is None:
        query = {}
    if headers is None:
        headers = {}

    # make full path if not given
    if url and url[:4] != "http":
        if url[0] == '/':  # can call with /resource if you want
            url = url[1:]
        url = self.full_path(url, api_version)
    elif not url:  # blank path
        url = self.full_path(url, api_version)

    qs = urlencode(query)
    if qs:
        qs = "?" + qs
    url += qs

    # mess with content
    if data:
        if not headers:  # assume JSON
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
        if headers and 'Content-Type' not in headers:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
    log.debug("%s %s" % (method, url))
    # make and send the request
    max_retries = 12
    retries = max_retries
    while retries > 0:
        try:
            response = self._session.request(
                method, url, data=data, timeout=self.timeout, headers=headers)
            break
        except (ConnectTimeout, ReadTimeout):
            retries -= 1
            if retries <= 0:
                raise
            else:
                time.sleep(12)
        except ConnectionError:
            retries -= 1
            if hasattr(self, '_reset_session'):
                self._reset_session()
            continue

    return response

apply_patch(Connection, 'make_request', make_request)
apply_patch(Connection, '_run_method', _run_method)
apply_patch(ApiResource, '_make_request', _make_request)
