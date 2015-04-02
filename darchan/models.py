# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class MatrixModel(models.Model):
    json_data = models.TextField(_('JSON serialized matrix'))
    depth = models.PositiveSmallIntegerField(_('Depth'))
    size = models.PositiveIntegerField(_('Size'))

    complete_mediation = models.BooleanField(
        _('Complete mediation'), default=False)
    economy_of_mechanism = models.BooleanField(
        _('Economy of mechanism'), default=False)
    layered_architecture = models.BooleanField(
        _('Layered architecture'), default=False)
    least_common_mechanism = models.BooleanField(
        _('Least common mechanism'), default=False)
    least_privileges = models.BooleanField(
        _('Least privileges'), default=False)
    open_design = models.BooleanField(
        _('Open design'), default=False)
    code_clean = models.BooleanField(
        _('Code clean'), default=False)
    separation_of_privileges = models.BooleanField(
        _('Separation of privileges'), default=False)

    builder = models.ForeignKey('MatrixBuilderModel',
                                verbose_name=_('Builder'),
                                related_name='matrices')


class MatrixBuilderModel(models.Model):
    created = models.DateTimeField(_('Creation date'), auto_now=True)
    groups = models.TextField(_('Groups', ))
    max_depth = models.PositiveSmallIntegerField(_('Maximum depth'))

    def __unicode__(self):
        return '%s' % self.created
