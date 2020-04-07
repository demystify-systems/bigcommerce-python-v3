# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import bigcommerce

from bigcommerce_v3.resources.base import *


class CatalogVariants(ListableApiResource, BaseV3):
    resource_name = 'catalog/variants'


class CatalogSummary(ListableApiResource, BaseV3):
    resource_name = 'catalog/summary'
