# -*- coding: utf-8 -*-
from django.conf import settings

PACKAGE_LIST = getattr(
    settings, "DARCHAN_PACKAGE_LIST", getattr(
        settings, "INSTALLED_APPS", ''))

