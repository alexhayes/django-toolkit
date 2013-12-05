from __future__ import absolute_import
from django.core.paginator import Paginator, Page
import collections

class RangeBasedPaginator(Paginator):
    
    def __init__(self, object_count, *args, **kwargs):
        """
        @todo Creating a range of values is really a waste of cycles...
        """
        object_list = range(1, object_count + 1)
        super(RangeBasedPaginator, self).__init__(object_list, *args, **kwargs)