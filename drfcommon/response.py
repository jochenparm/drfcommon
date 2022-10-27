#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
from rest_framework.response import Response


def make_data(code=200, describe='', **kwargs):
    """

    :param describe:
    :param code: 200(成功), 101(参数错误), 199(其他)
    :return:
    """
    resp = dict(
        code=code,
        describe=describe, **kwargs
    )
    return resp


def make_response(code=200, describe='成功', **kwargs):
    """

    :param describe:
    :param code: 200(成功), 101(参数错误), 199(其他),
    :return:
    """
    data = make_data(code=code, describe=describe, **kwargs)
    return Response(data)


def done(code=200, describe='成功', **kwargs):
    """

    :param code:
    :param describe:
    :param kwargs:
    :return:
    """
    data = make_response(
        code=code, describe=describe,
        **kwargs
    )
    return data
