from __future__ import absolute_import
from django_toolkit.db.models import QuerySetManager
from mptt.managers import TreeManager

class TreeQuerySetManager(QuerySetManager, TreeManager): pass