#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
import logging

from rest_framework.viewsets import ModelViewSet
from drfcommon.exceptions import com_exception_handler
from drfcommon.pagination import ComStandardPagination
from drfcommon.response import done


logger = logging.getLogger("debug")


class ComApiMixin:
    @staticmethod
    def get_exception_handler():
        """
        Returns the exception handler that this view uses.
        """
        return com_exception_handler

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        logger.debug(
            "initialize_request:header:{}".format(request.headers))
        logger.debug("initialize_request:body:{}".format(request.body))
        return super().initialize_request(request, *args, **kwargs)

    @staticmethod
    def errors(errors):
        logger.error("err:{}".format(errors))
        code = 400
        return done(
            code=code,
            describe='请检查请求参数',
            errors=errors,
            data=None
        )

    def do_request(self, request):
        """

        :param request:
        :return: resp, err
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(u'serializer err:{}'.format(serializer.errors))
            return None, serializer.errors
        validated_data = serializer.validated_data
        return validated_data, None


class AllowAnyModelViewSet(ModelViewSet):
    """
    AllowAny  ModelViewSet
    """
    http_method_names = ['get', 'post', 'put', 'delete', 'options', ]
    serializer_map = dict()

    def get_serializer_class(self):
        if not isinstance(self.serializer_map, dict):
            return self.serializer_class
        if self.action not in self.serializer_map:
            logger.warning('action:{} not conf serializer'.format(self.action))
        return self.serializer_map.get(self.action, self.serializer_class)


class ComApiBaseModelSet(AllowAnyModelViewSet, ComApiMixin):
    """
    Com App Base ModelViewSet

    base method:
    1.get_exception_handler
    2.initialize_request
    3.errors
    4.done

    restful method:
    1.list:
    2.retrieve
    3.update
    4.create
    """
    pagination_class = ComStandardPagination

    def destroy(self, request, *args, **kwargs):
        """
        删除: 通过主键id

        ----

        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return done()

    def perform_destroy(self, instance):
        """
        删除: 逻辑删除
        :param instance:
        :return:
        """
        instance.is_deleted = True
        instance.save()

    def list(self, request, *args, **kwargs):
        """
        列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return done(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return done(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        更新
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid():
            logger.error('serializer err:{}'.format(serializer.errors))
            return self.errors(serializer.errors)
        validated_data = serializer.validated_data
        # 更新逻辑: 由调用方序列化定制
        serializer.update(instance, validated_data)
        return done(data=validated_data)

    def create(self, request, *args, **kwargs):
        """
        创建
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error('serializer err:{}'.format(serializer.errors))
            return self.errors(serializer.errors)
        validated_data = serializer.validated_data
        # 创建逻辑: 由调用方序列化定制
        instance = serializer.create(validated_data)
        # data = validated_data
        data = dict()
        data['id'] = instance.id
        return done(data=data)

    def bulk_create(self, request, *args, **kwargs):
        """
        批量创建
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error('serializer err:{}'.format(serializer.errors))
            return self.errors(serializer.errors)
        validated_data = serializer.validated_data
        instance_list = serializer.create(validated_data)
        data = dict()
        data['id_list'] = [instance.id for instance in instance_list]
        return done(data=data)