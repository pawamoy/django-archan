# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from darchan.models import MatrixModel, MatrixBuilderModel


admin.site.register(MatrixModel)
admin.site.register(MatrixBuilderModel)
