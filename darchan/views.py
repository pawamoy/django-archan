# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import range
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from darchan.utils import generate_matrix
from darchan.app_settings import PACKAGE_LIST, TEMPLATE
from darchan.models import MatrixBuilderModel, MatrixModel

# FIXME: too much repetition, apply DRY


@staff_member_required
def v_generate_matrix(request):
    builder, matrices = generate_matrix(PACKAGE_LIST)
    return v_view_matrix(request, builder.pk, 1)


@staff_member_required
def v_view_last_matrix(request):
    return v_view_matrix(request, -1, 1)


@staff_member_required
def v_view_matrix(request, builder_id, depth):
    history = MatrixBuilderModel.objects.all()
    if history.count() > 0:
        depth = int(depth)
        try:
            if builder_id == -1:
                builder = history.order_by('-created')[0]
            else:
                builder = MatrixBuilderModel.objects.get(pk=builder_id)
            matrix = builder.matrices.get(depth=depth)
        except (MatrixBuilderModel.DoesNotExist, MatrixModel.DoesNotExist):
            return render(request, TEMPLATE, {
                'matrix': None,
                'history': history
            })
        return render(request, TEMPLATE, {
            'builder': builder,
            'matrix': matrix,
            'max_depth': list(range(1, builder.max_depth+1)),
            'history': history.exclude(pk=builder_id)
        })
    else:
        return v_generate_matrix(request)


@staff_member_required
def v_download_csv(request, builder_id, depth):
    try:
        builder = MatrixBuilderModel.objects.get(pk=builder_id)
        matrix = builder.matrices.get(depth=depth)

        # Create the HttpResponse object with the appropriate CSV data & header
        response = HttpResponse(matrix.csv_data, content_type='text/csv')
        attachment = 'attachment; filename="matrix-%s-depth-%s.csv"' % (
            builder.created.strftime('%Y-%b-%d'), depth)
        response['Content-Disposition'] = attachment
        return response
    except (MatrixBuilderModel.DoesNotExist, MatrixModel.DoesNotExist):
        return render(request, TEMPLATE,
                      {'matrix': None,
                       'history': MatrixBuilderModel.objects.all()})

