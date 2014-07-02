from __future__ import absolute_import
from django_toolkit.db.models import QuerySetManager
from model_utils.managers import InheritanceManager

class InheritanceQuerySetManager(QuerySetManager, InheritanceManager): pass
