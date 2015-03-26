# -*- coding: utf-8 -*-
import sys
from dependenpy.utils import DependencyMatrix
from darchan.models import DependencyMatrixModel


def get_django_module_path(mod):
    mod_path = sys.modules.get(mod)
    if mod_path:
        return 'py'.join(mod_path.__file__.rsplit('pyc'))
    return None


def generate_matrix(apps):
    matrix = DependencyMatrix(apps, get_django_module_path)
    matrix.build()
    return DependencyMatrixModel.objects.create(json=matrix.to_json())
