#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
from rest_framework.response import Response


def make_data(code=200, message='', **kwargs):
    """

    :param message:
    :param code: 200(成功), 101(参数错误), 199(其他)
    :return:
    """
    if "data" not in kwargs:
        kwargs["data"] = dict()
    if "items" not in kwargs:
        kwargs["items"] = list()

    resp = dict(
        code=code,
        message=message,
        **kwargs
    )
    return resp


def make_response(code=200, message='成功', **kwargs):
    """

    :param message:
    :param code: 200(成功), 101(参数错误), 199(其他),
    :return:
    """
    data = make_data(code=code, message=message, **kwargs)
    return Response(data)


def done(code=200, message='成功', **kwargs):
    """

    :param code:
    :param message:
    :param kwargs:
    :return:
    """
    data = make_response(
        code=code,
        message=message,
        **kwargs
    )
    return data
