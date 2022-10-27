#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doc:
"""
import logging

from drfhumplib.parsers import SnakeJSONParser
from drfhumplib.renders import HumpJSONRenderer

from drfcommon.view_base import AllowAnyModelViewSet, ComApiMixin

logger = logging.getLogger("debug")


class AllowAnyHumpModelViewSet(AllowAnyModelViewSet):
    """
    AllowAny Hump ModelViewSet
    """
    parser_classes = (SnakeJSONParser,)
    renderer_classes = (HumpJSONRenderer,)


class ComApiBaseModelSet(AllowAnyHumpModelViewSet, ComApiMixin):
    pass
