#!/usr/bin/env python
"""
pagination.py
"""

from collections import OrderedDict

import six
import logging
from django.core.paginator import InvalidPage
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from drfcommon.response import make_response

logger = logging.getLogger("debug")


class StandardPagination(PageNumberPagination):
    """
    Standard Pagination
    """
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 150

    @staticmethod
    def fix_link(link=''):
        """

        :param link:
        :return:
        """
        # 线上使用
        if not link:
            return link
        if not link.startswith('https'):
            link = link.replace('http', 'https')
        return link

    def get_paginated_response(self, data):
        errcode = 0
        errmsg = ''
        # 通常data => query_set
        if isinstance(data, dict):
            if data.get('errcode'):
                errcode = data.get('errcode')
            if data.get('errmsg'):
                errmsg = data.get('errmsg')
        next_link = self.get_next_link()
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            # ('_next', next_link),
            ('next', self.fix_link(link=next_link)),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('errcode', errcode),
            ('errmsg', errmsg),
        ]))


class ComStandardPagination(PageNumberPagination):
    """
    Com Standard Pagination
    """
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 150

    def paginate_queryset(self, queryset, request, view=None):
        """

        :param queryset:
        :param request:
        :param view:
        :return:
        """
        page_size = request.query_params.get(
            self.page_size_query_param, self.page_size)
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            logger.warning("msg:{}".format(msg))
            # raise NotFound(msg)
            return None
        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True
        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        total_size = self.page.paginator.count
        next_link = self.get_next_link()
        return make_response(
            total=total_size,
            data={},
            items=data,
            next_link=next_link,
        )


class ComPagination(ComStandardPagination):
    page_size = 50

    def get_paginated_response(self, data):
        total_size = self.page.paginator.count
        next_link = self.get_next_link()
        return make_response(
            totalSize=total_size,
            body=dict(orderInfoItems=data),
            next_link=next_link,
        )
