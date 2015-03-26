# -*- coding: utf-8 -*-
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from dependenpy.utils import MatrixBuilder


class MatrixModel(models.Model):
    json_data = models.TextField(_('JSON serialized matrix'))
    depth = models.PositiveSmallIntegerField(_('Depth'))
    size = models.PositiveIntegerField(_('Size'))
    builder = models.ForeignKey('MatrixBuilderModel',
                                verbose_name=_('Builder'),
                                related_name='matrices')


class MatrixBuilderModel(models.Model):
    created = models.DateTimeField(_('Creation date'), auto_now=True)
    groups = models.TextField(_('Groups', ))
    max_depth = models.PositiveSmallIntegerField(_('Maximum depth'))

    def __unicode__(self):
        return '%s' % self.created
