# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import json
from builtins import range
from dependenpy.utils import MatrixBuilder
from archan.dsm import DesignStructureMatrix
from archan.checker import Archan
from darchan.models import MatrixModel, MatrixBuilderModel


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
    compute its different sorting orders, and return a database
    instance of the builder and its matrices.


    :param apps: str/list/OrderedDict, the list of packages to scan
    :return: :class:`MatrixBuilderModel`, [:class:`MatrixModel`]; the builder
        and its matrices (database objects)
    """

    builder = MatrixBuilder(apps, get_django_module_path)
    builder.build()
    matrix = builder.get_matrix(1)
    matrix.compute_orders()
    # for matrix in builder.matrices:
    #     matrix.compute_orders()

    dsm_list = [DesignStructureMatrix(m.groups, m.keys, m.matrix)
                for m in builder.matrices]
    archan = Archan()

    return create_instance(builder, [archan.check_all(dsm)
                                     for dsm in dsm_list])


def create_instance(builder, archans):
    """Save the builder instance and its matrices as database objects
    and return them.

    :type builder: :class:`MatrixBuilder`
    :param builder: the builder instance from dependenpy
    :return: :class:`MatrixBuilderModel`, [:class:`MatrixModel`]; the builder
        and its matrices (database objects)
    """

    builder_db = MatrixBuilderModel.objects.create(
        max_depth=builder.max_depth,
        groups=json.dumps(builder.groups))

    matrices_db = []
    # for matrix, archan in builder.matrices, archans:
    for i in range(builder.max_depth):
        matrices_db.append(
            MatrixModel.objects.create(
                depth=builder.matrices[i].depth,
                size=builder.matrices[i].size,
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

    return builder_db, matrices_db
