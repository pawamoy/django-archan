# -*- coding: utf-8 -*-
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from dependenpy.utils import DependencyMatrix


class DependencyMatrixModel(models.Model):
    json = models.TextField(_('JSON serialized matrix'))
    created = models.DateTimeField(_('Creation date'), auto_now=True)

    def to_obj(self):
        return json.loads(self.json)

    def get_instance(self):
        data = self.to_obj()
        dm = DependencyMatrix(data['packages'])
        dm.groups = data['groups']
        dm.modules = data['modules']
        dm.imports = data['imports']
        dm.matrices = data['matrices']
        dm.max_depth = data['max_depth']
        dm._inside = data['_inside']
        dm._modules_are_built = data['_modules_are_built']
        dm._imports_are_built = data['_imports_are_built']
        dm._matrices_are_built = data['_matrices_are_built']
        return dm

    def level(self, level):
        return json.dumps(
            self.get_instance().matrix_to_json(level, FILTER_OPTIONS))

    def __unicode__(self):
        return '%s' % self.created
