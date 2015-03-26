# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from darchan.utils import generate_matrix
from darchan.app_settings import PACKAGE_LIST
from darchan.models import DependencyMatrixModel

# FIXME: too much repetition, apply DRY


@staff_member_required
def v_generate_matrix(request):
    matrix_obj = generate_matrix(PACKAGE_LIST)
    return v_view_matrix(request, matrix_obj.pk, 1)


@staff_member_required
def v_view_last_matrix(request):
    history = DependencyMatrixModel.objects.all()
    if history.count() > 0:
        matrix_obj = DependencyMatrixModel.objects.order_by('-created')[0]
        instance = matrix_obj.get_instance()
        matrix_json = instance.matrix_to_json(1)
        return render(request, 'matrix/view_matrix.html', {
            'matrix': matrix_obj,
            'matrix_json': matrix_json,
            'groups': json.dumps(instance.groups),
            'level': 1,
            'size': len(instance.get_matrix(1)['modules']),
            'max_depth': range(1, instance.max_depth+1),
            'history': history.exclude(pk=matrix_obj.pk)
        })
    else:
        return v_generate_matrix(request)


@staff_member_required
def v_view_matrix(request, mid, lvl):
    history = DependencyMatrixModel.objects.all()
    if history.count() > 0:
        lvl = int(lvl)
        try:
            matrix_obj = DependencyMatrixModel.objects.get(pk=mid)
            instance = matrix_obj.get_instance()
            matrix_json = instance.matrix_to_json(lvl)
        except DependencyMatrixModel.DoesNotExist:
            return render(request, 'matrix/view_matrix.html',
                          {'matrix_json': None})
        return render(request, 'matrix/view_matrix.html', {
            'matrix': matrix_obj,
            'matrix_json': matrix_json,
            'groups': json.dumps(instance.groups),
            'level': lvl,
            'size': len(instance.get_matrix(lvl)['modules']),
            'max_depth': range(1, instance.max_depth+1),
            'history': history.exclude(pk=matrix_obj.pk)
        })
    else:
        return v_generate_matrix(request)


@staff_member_required
def v_download_csv(request, mid, lvl):
    try:
        matrix_obj = DependencyMatrixModel.objects.get(pk=mid)
        instance = matrix_obj.get_instance()

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        attachment = 'attachment; filename="matrix-%s-lvl-%s.csv"' % (
            matrix_obj.created, lvl)
        response['Content-Disposition'] = attachment

        return instance.matrix_to_csv(lvl, response)
    except DependencyMatrixModel.DoesNotExist:
        return render(request, 'matrix/view_matrix.html',
                      {'matrix_json': None})
