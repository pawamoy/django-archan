# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from django.conf.urls import url
from darchan import views

urlpatterns = [
    url(r'^view_matrix/$',
        views.v_view_last_matrix, name='view_last_matrix'),
    url(r'^view_matrix/(?P<builder_id>\d+)/(?P<depth>\d+)/$',
        views.v_view_matrix, name='view_matrix'),
    url(r'^generate_matrix/$',
        views.v_generate_matrix, name='generate_matrix'),
    url(r'^download_csv/(?P<builder_id>\d+)/(?P<depth>\d+)/$',
        views.v_download_csv, name='download_csv'),
]
