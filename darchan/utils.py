# -*- coding: utf-8 -*-
import sys
import json
from dependenpy.utils import MatrixBuilder
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
    for matrix in builder.matrices:
        matrix.compute_orders()
    return create_instance(builder)


def create_instance(builder):
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
    for matrix in builder.matrices:
        matrices_db.append(
            MatrixModel.objects.create(
                depth=matrix.depth,
                size=matrix.size,
                builder=builder_db,
                json_data=json.dumps(
                    {'modules': matrix.modules.values(),
                     'dependencies': matrix.dependencies})))

    return builder_db, matrices_db
