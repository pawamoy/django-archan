# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import json
import os
from builtins import range
from dependenpy.utils import MatrixBuilder
import archan
from archan.dsm import DesignStructureMatrix
from archan.checker import Archan
from darchan.models import MatrixModel, MatrixBuilderModel, Criterion


def get_django_module_path(mod):
    """A method to determine the path of a module within a Django project.

    :param mod: str, the module name
    :return: str, the absolute path to the module
    """

    mod_path = sys.modules.get(mod)
    if mod_path:
        return 'py'.join(mod_path.__file__.rsplit('pyc'))
    return None


def generate_matrix(apps):
    """Build a matrix using MatrixBuilder from dependenpy,
    compute the different sorting orders and check the archan criteria
    for each of its matrices and return a database instance of the builder
    and its matrices.

    :param apps: str/list/OrderedDict, the list of packages to scan
    :return: :class:`MatrixBuilderModel`, the builder (database object)
    """

    builder = MatrixBuilder(apps, get_django_module_path)
    builder.build()
    matrix = builder.get_matrix(1)
    matrix.compute_orders()
    # for matrix in builder.matrices:
    #     matrix.compute_orders()

    sorts_list = [','.join([key for key, value in m.orders.iteritems()
                            if value[0]])
                  for m in builder.matrices]
    dsm_list = [DesignStructureMatrix(m.groups, m.keys, m.matrix)
                for m in builder.matrices]
    archan = Archan()

    return create_instance(builder, sorts_list, [archan.check_all(dsm)
                                                 for dsm in dsm_list])


def create_instance(builder, sorts, archans):
    """Save the builder instance and its matrices as database objects
    and return them.

    :type builder: :class:`MatrixBuilder`
    :param builder: the builder instance from dependenpy
    :param sorts: list of str, comma joined available sorts for each matrix
    :param archans: list of dict, archan checker results for each matrix
    :return: :class:`MatrixBuilderModel`, the builder (database object)
    """

    builder_db = MatrixBuilderModel.objects.create(
        max_depth=builder.max_depth,
        groups=json.dumps(builder.groups))

    matrices_db = []
    for i in range(builder.max_depth):
        matrices_db.append(
            MatrixModel.objects.create(
                depth=builder.matrices[i].depth,
                size=builder.matrices[i].size,
                sorts=sorts[i],
                builder=builder_db,
                json_data=json.dumps(
                    {'modules': list(builder.matrices[i].modules.values()),
                     'dependencies': builder.matrices[i].dependencies}),
                csv_data=builder.matrices[i].to_csv(),
                complete_mediation=archans[i]['CM'],
                economy_of_mechanism=archans[i]['EOM'],
                separation_of_privileges=archans[i]['SOP'],
                layered_architecture=archans[i]['LA'],
                least_common_mechanism=archans[i]['LCM'],
                least_privileges=archans[i]['LP'],
                open_design=archans[i]['OD'],
                code_clean=archans[i]['CC']
            ))

    return builder_db


def get_criterion(criterion):
    """Return the database object containing the criterion cap-first'd name
    and its description. If the object does not exist, this function tries
    to create it using a text file inside the criteria directory of archan
    package.

    :param criterion: str, name of the criterion. Can be like 'My Criterion'
        or 'my_criterion'
    :return: :class:`Criterion`, the criterion database object
    """

    criterion = criterion.lower().replace(' ', '_')

    try:
        return Criterion.objects.get(name=criterion)
    except Criterion.DoesNotExist:
        paper_dir = os.path.abspath(
            os.path.join(os.path.dirname(archan.__file__), 'criteria'))
        try:
            with open(os.path.join(paper_dir, criterion+'.txt')) as f:
                return Criterion.objects.create(
                    name=criterion,
                    description=f.read())
        except IOError:
            raise AttributeError('No criterion named %s' % criterion)
