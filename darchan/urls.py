# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'darchan.views',
    url(r'^view_matrix/$', 'v_view_last_matrix', name='view_last_matrix'),
    url(r'^view_matrix/(?P<builder_id>\d+)/(?P<depth>\d+)/$', 'v_view_matrix',
        name='view_matrix'),
    url(r'^generate_matrix/$', 'v_generate_matrix', name='generate_matrix'),
    url(r'^download_csv/(?P<builder_id>\d+)/(?P<depth>\d+)/$',
        'v_download_csv', name='download_csv'),
)
