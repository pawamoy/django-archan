# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


# FIXME: we should maybe store archan criteria result in the builder model
# since each matrix depth should have the same results (not sure)
class MatrixModel(models.Model):
    """The database model containing the data of a dependenpy.Matrix class
    instance. It does not store all the data but only JSON data that are
    needed by d3js and group sorted CSV data (no other sorts).
    """

    json_data = models.TextField(_('JSON serialized matrix'))
    csv_data = models.TextField(_('CSV data'))
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

    def __unicode__(self):
        return '%s / Depth %s' % (self.builder, self.depth)


class MatrixBuilderModel(models.Model):
    """The database model containing the data of a dependenpy.MatrixBuilder
    class instance. It contains the date of creation of the instance, the
    groups given by the user (as settings), and the maximum depth.
    """

    created = models.DateTimeField(_('Creation date'), auto_now=True)
    groups = models.TextField(_('Groups', ))
    max_depth = models.PositiveSmallIntegerField(_('Maximum depth'))

    def __unicode__(self):
        return '%s' % self.created.strftime('%Y-%b-%d')
