# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import os

import bigcommerce

from bigcommerce_v3 import resources
from bigcommerce_v3 import connection

class BigcommerceApi(bigcommerce.api.BigcommerceApi):
    def __init__(
        self, host=None, basic_auth=None, client_id=None, store_hash=None, access_token=None,
        rate_limiting_management=None, max_retries=6):
        self.api_service = os.getenv('BC_API_ENDPOINT', 'api.bigcommerce.com')
        self.auth_service = os.getenv('BC_AUTH_SERVICE', 'login.bigcommerce.com')

        if host and basic_auth:
            self.connection = connection.Connection(host, basic_auth, max_retries=max_retries)
        elif client_id and store_hash:
            if not rate_limiting_management:
                rate_limiting_management = {'min_requests_remaining': 3, 'wait': True}
            self.connection = connection.OAuthConnection(
                client_id, store_hash, access_token, self.api_service,
                rate_limiting_management=rate_limiting_management, max_retries=max_retries)
        else:
            raise Exception(
                "Must provide either (client_id and store_hash) or (host and basic_auth)")

    def __getattr__(self, item):
        return ApiResourceWrapper(item, self)


class ApiResourceWrapper(bigcommerce.api.ApiResourceWrapper):
    @classmethod
    def str_to_class(cls, str):
        """
        Transforms a string class name into a class object
        Assumes that the class is already loaded.
        """
        if hasattr(resources, str):
            obj = getattr(resources, str)
        else:
            obj = getattr(bigcommerce.resources, str)

        return obj
