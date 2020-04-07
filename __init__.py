# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

API_V2_BASIC_AUTH_PATH = '/api/v2/{}'
API_V2_OAUTH_PATH = '/stores/{}/v2/{}'
API_V3_BASIC_AUTH_PATH = '/api/v3/{}'
API_V3_OAUTH_PATH = '/stores/{}/v3/{}'

import sys
import logging

from bigcommerce_v3 import monkey_patches
from bigcommerce_v3 import api
from bigcommerce_v3 import connection

import bigcommerce

bigcommerce.connection.log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
bigcommerce.connection.log.addHandler(stream_handler)
