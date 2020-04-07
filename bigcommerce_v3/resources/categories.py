# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import bigcommerce
from bigcommerce_v3.resources.base import *


class Categories(bigcommerce.resources.categories.Categories, BaseV3):
    resource_name = 'catalog/categories'


class CategoryMetaFields(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'metafields'
    parent_resource = 'catalog/categories'
    parent_key = 'category_id'


class CategoryImages(CreateableApiSubResource, DeleteableApiSubResource, BaseV3):
    resource_name = 'image'
    parent_resource = 'catalog/categories'
    parent_key = 'category_id'
