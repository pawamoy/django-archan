# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings

PACKAGE_LIST = getattr(
    settings, 'DARCHAN_PACKAGE_LIST', getattr(
        settings, 'INSTALLED_APPS', ''))

TEMPLATE = getattr(
    settings, 'DARCHAN_TEMPLATE',
    'darchan/matrix.html')
