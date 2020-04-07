# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import bigcommerce

from bigcommerce_v3.resources.base import *


class Products(bigcommerce.resources.products.Products, BaseV3):
    resource_name = 'catalog/products'

    def variants(self, id=None):
        if id:
            return ProductVariants(self.id, id, connection=self._connection)
        else:
            return ProductVariants.all(self.id, connection=self._connection)

    def metafields(self, id=None):
        if id:
            return ProductMetafields(self.id, id, connection=self._connection)
        else:
            return ProductMetafields.all(self.id, connection=self._connection)

    def options(self, id=None):
        if id:
            return ProductOptions(self.id, id, connection=self._connection)
        else:
            return ProductOptions.all(self.id, connection=self._connection)


class ProductMetafields(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'metafields'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'


class ProductBulkPricingRules(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'bulk-pricing-rules'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'


class ProductCustomFields(bigcommerce.resources.products.ProductCustomFields, BaseV3):
    resource_name = 'custom-fields'
    parent_resource = 'catalog/products'


class ProductImages(bigcommerce.resources.products.ProductImages, BaseV3):
    parent_resource = 'catalog/products'


class ProductOptions(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource, BaseV3):
    resource_name = 'options'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'


class ProductOptionValues(ApiResource, BaseV3):
    resource_name = 'values'

    @classmethod
    def all(cls, productid, optionid, connection=None, **params):
        all_path = '{}/{}/{}/{}/{}'.format(
            Products.resource_name, productid, ProductOptions.resource_name, optionid,
            cls.resource_name)
        response = cls._make_request('GET', all_path, connection, **params)

        attrs = {'product_id': productid, 'option_id': optionid}
        if response and not isinstance(response, dict):
            [obj.update(attrs) for obj in response]
        else:
            response.update(attrs)

        return cls._create_object(response, connection=connection)

    @classmethod
    def create(cls, productid, optionid, connection=None, **params):
        create_path = '{}/{}/{}/{}/{}'.format(
            Products.resource_name, productid, ProductOptions.resource_name, optionid,
            cls.resource_name)
        response = cls._make_request('POST', create_path, connection, data=params)
        response.update({'product_id': productid, 'option_id': optionid})

        return cls._create_object(response, connection=connection)

    @classmethod
    def get(cls, productid, optionid, id, connection=None, **params):
        get_path = '{}/{}/{}/{}/{}/{}'.format(
            Products.resource_name, productid, ProductOptions.resource_name, optionid,
            cls.resource_name, id)
        response = cls._make_request('GET', get_path, connection, params=params)
        response.update({'product_id': productid, 'option_id': optionid})

        return cls._create_object(response, connection=connection)

    def update(self, **updates):
        update_path = '{}/{}/{}/{}/{}/{}'.format(
            Products.resource_name, self.product_id, ProductOptions.resource_name, self.option_id,
            self.resource_name, self.id)
        response = self._make_request('PUT', update_path, self._connection, data=updates)
        return self._create_object(response, connection=self._connection)

    def delete(self):
        delete_path = '{}/{}/{}/{}/{}/{}'.format(
            Products.resource_name, self.product_id, ProductOptions.resource_name, self.option_id,
            self.resource_name, self.id)
        return self._make_request('DELETE', delete_path, self._connection)


class ProductVariants(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'variants'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'


# TODO
class ProductVariantMetafields(BaseV3):
    pass


class ProductModifiers(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'modifiers'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'


# TODO
class ProductModifierValues(BaseV3):
    pass


# TODO
class ProductModifierImages(BaseV3):
    pass


class ProductComplexRules(ListableApiSubResource, CreateableApiSubResource,
    UpdateableApiSubResource, DeleteableApiSubResource,
    CollectionDeleteableApiSubResource, BaseV3):
    resource_name = 'complex-rules'
    parent_resource = 'catalog/products'
    parent_key = 'product_id'


class ProductReviews(bigcommerce.resources.products.ProductReviews, BaseV3):
    parent_resource = 'catalog/products'


class ProductVideos(bigcommerce.resources.products.ProductVideos, BaseV3):
    parent_resource = 'catalog/products'
