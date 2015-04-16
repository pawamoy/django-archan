# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from darchan.models import MatrixModel, MatrixBuilderModel, Criterion


class MatrixModelInline(admin.TabularInline):
    model = MatrixModel
    extra = 0
    verbose_name = 'Individual Members'
    exclude = ('sorts', 'json_data', 'csv_data')
    readonly_fields = ('depth', 'size')


class MatrixBuilderAdmin(admin.ModelAdmin):
    inlines = (MatrixModelInline,)


admin.site.register(MatrixModel)
admin.site.register(Criterion)
admin.site.register(MatrixBuilderModel, MatrixBuilderAdmin)
