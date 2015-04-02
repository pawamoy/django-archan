# -*- coding: utf-8 -*-
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
            'max_depth': range(1, builder.max_depth+1),
            'history': history.exclude(pk=builder_id)
        })
    else:
        return v_generate_matrix(request)


@staff_member_required
def v_download_csv(request, builder_id, depth):
    try:
        matrix_obj = MatrixBuilderModel.objects.get(pk=builder_id)
        instance = matrix_obj.get_instance()

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        attachment = 'attachment; filename="matrix-%s-lvl-%s.csv"' % (
            matrix_obj.created, depth)
        response['Content-Disposition'] = attachment

        return instance.matrix_to_csv(depth, response)
    except MatrixBuilderModel.DoesNotExist:
        return render(request, TEMPLATE,
                      {'matrix_json': None})

