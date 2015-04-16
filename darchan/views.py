# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import range
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from darchan.utils import generate_matrix, get_criterion
from darchan.app_settings import PACKAGE_LIST, TEMPLATE
from darchan.models import MatrixBuilderModel, MatrixModel


@staff_member_required
def v_generate_matrix(request):
    """Generate a new matrix and return the view to display it.

    :param request: Django request object
    :return: a view
    """

    builder, matrices = generate_matrix(PACKAGE_LIST)
    return v_view_matrix(request, builder.pk, 1)


@staff_member_required
def v_view_last_matrix(request):
    """Return the view to display the last generated matrix.
    Just a shortcut for v_view_matrix(request, -1, 1).

    :param request: Django request object
    :return: a view
    """
    return v_view_matrix(request, -1, 1)


@staff_member_required
def v_view_matrix(request, builder_id, depth):
    """Return the view to display the specified matrix.

    If the builder id is equal to -1, then the selected builder is the last
    generated one, and the selected depth is 1.

    If the builder can't be found in the database, only the history of
    builders will be display in the HTML page.

    If no matrix were previously generated, then the generator is called
    and the new matrix is returned in this view.

    :param request: Django request object
    :param builder_id: int, DB builder object id
    :param depth: int, depth of the requested matrix
    :return: a view
    """

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
            'history': history.exclude(pk=builder_id),
            'criteria': [{'object': get_criterion(c),
                          'value': matrix.criterion_value(c)}
                         for c in MatrixModel.criteria_names()]
        })
    else:
        return v_generate_matrix(request)


@staff_member_required
def v_download_csv(request, builder_id, depth):
    """Create a file containing the matrix in a CSV format and send it
    to the user as a downloadable file.

    :param request: Django request object
    :param builder_id: int, DB builder object id
    :param depth: int, depth of the requested matrix
    :return: a file containing the CSV data (group sorted)
    """

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
