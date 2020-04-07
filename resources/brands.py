# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import bigcommerce
from bigcommerce_v3.resources.base import *


class Brands(bigcommerce.resources.brands.Brands, BaseV3):
    resource_name = 'catalog/brands'


class BrandMetafields(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'metafields'
    parent_resource = 'catalog/brands'
    parent_key = 'brand_id'


class BrandImages(CreateableApiSubResource, DeleteableApiSubResource, BaseV3):
    resource_name = 'image'
    parent_resource = 'catalog/brands'
    parent_key = 'brand_id'
