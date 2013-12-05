from django.template import Library, Node, TemplateSyntaxError

# @see http://djangosnippets.org/snippets/2877/

register = Library()

class _SlicedPaginator:
    def __init__(self, curpage, npages, maxpages_items):
        """Contructor.
        
        Example:
        >>> _SlicedPaginator(1, 3, 3)
        _SlicedPaginator(curpage=1, npages=3, maxpages_items=3)
        """
        self.curpage = int(curpage)
        self.npages = int(npages)
        self.maxpages_items = int(maxpages_items)
        assert 1 <= self.curpage <= self.npages, "%s %s" % (self.curpage,
                                                            self.npages)
        assert self.maxpages_items > 0
        assert self.maxpages_items % 2 == 1, "Only uneven maxpages_items supported. Unclear how to be presented otherwise."
        self.max_prev_items = (self.maxpages_items - 1) / 2
        self.max_next_items = self.max_prev_items
        
    def __repr__(self):
        tmpl = "_SlicedPaginator(curpage={0}, npages={1}, maxpages_items={2})"
        return tmpl.format(self.curpage, self.npages, self.maxpages_items)
        
    def _build_full_list(self):
        """Build a full list of pages.
        
        Examples:
        >>> _SlicedPaginator(1, 7, 5)._build_full_list()
        [1, 2, 3, 4, 5]
        >>> _SlicedPaginator(6, 7, 5)._build_full_list()
        [3, 4, 5, 6, 7]
        >>> _SlicedPaginator(6, 7, 5)._build_full_list()
        [3, 4, 5, 6, 7]
        >>> import itertools
        >>> combinations = itertools.combinations(range(100), 2)
        >>> combinations = filter(lambda (x,y): x<y, combinations)
        >>> for page, maxpages in combinations:
        ...     a = _SlicedPaginator(page + 1, maxpages, 7)
        ...     b = a._build_full_list()
        >>> _SlicedPaginator(2, 5, 7)._build_full_list()
        [1, 2, 3, 4, 5]
        >>> _SlicedPaginator(5, 5, 7)._build_full_list()
        [1, 2, 3, 4, 5]
        """
        if self.npages <= self.maxpages_items:
            return range(1, self.npages + 1)
        else:
            l = range(self.curpage - self.max_prev_items,
                      self.curpage + self.max_next_items + 1)
            while l and l[0] < 1:
                l.append(l[-1] + 1)
                del l[0]
            while l and l[-1] > self.npages:
                l.insert(0, l[0] - 1)
                del l[-1]
            return l
            
    
    def prev_pages(self):
        """Get the previous pages.
        
        Example:
        >>> map(lambda i: _SlicedPaginator(i, 6, 3).prev_pages(), range(1, 7))
        [[], [1], [2], [3], [4], [4, 5]]
        >>> map(lambda i: _SlicedPaginator(i, 7, 3).prev_pages(), range(1, 8))
        [[], [1], [2], [3], [4], [5], [5, 6]]
        >>> map(lambda i: _SlicedPaginator(i, 6, 5).prev_pages(), range(1, 7))
        [[], [1], [1, 2], [2, 3], [2, 3, 4], [2, 3, 4, 5]]
        >>> map(lambda i: _SlicedPaginator(i, 7, 5).prev_pages(), range(1, 8))
        [[], [1], [1, 2], [2, 3], [3, 4], [3, 4, 5], [3, 4, 5, 6]]
        """
        return filter(lambda x: x < self.curpage, self._build_full_list())
    
    def hidden_prev_pages(self):
        """Check if the previous pages where sliced.
        
        Example:
        >>> map(lambda i: _SlicedPaginator(i, 6, 3).hidden_prev_pages(), range(1, 7))
        [False, False, True, True, True, True]
        >>> map(lambda i: _SlicedPaginator(i, 7, 3).hidden_prev_pages(), range(1, 8))
        [False, False, True, True, True, True, True]
        >>> map(lambda i: _SlicedPaginator(i, 6, 5).hidden_prev_pages(), range(1, 7))
        [False, False, False, True, True, True]
        >>> map(lambda i: _SlicedPaginator(i, 7, 5).hidden_prev_pages(), range(1, 8))
        [False, False, False, True, True, True, True]
        """
        prev_pages = self.prev_pages()
        return len(prev_pages) > 0 and prev_pages[0] > 1
        
    def next_pages(self):
        """Get the next pages.
        
        Example:
        >>> map(lambda i: _SlicedPaginator(i, 6, 3).next_pages(), range(1, 7))
        [[2, 3], [3], [4], [5], [6], []]
        >>> map(lambda i: _SlicedPaginator(i, 7, 3).next_pages(), range(1, 8))
        [[2, 3], [3], [4], [5], [6], [7], []]
        >>> map(lambda i: _SlicedPaginator(i, 6, 5).next_pages(), range(1, 7))
        [[2, 3, 4, 5], [3, 4, 5], [4, 5], [5, 6], [6], []]
        >>> map(lambda i: _SlicedPaginator(i, 7, 5).next_pages(), range(1, 8))
        [[2, 3, 4, 5], [3, 4, 5], [4, 5], [5, 6], [6, 7], [7], []]
        """
        return filter(lambda x: x > self.curpage, self._build_full_list())
    
    def hidden_next_pages(self):
        """Check if the next pages where sliced.
        
        Example:
        >>> map(lambda i: _SlicedPaginator(i, 6, 3).hidden_next_pages(), range(1, 7))
        [True, True, True, True, False, False]
        >>> map(lambda i: _SlicedPaginator(i, 7, 3).hidden_next_pages(), range(1, 8))
        [True, True, True, True, True, False, False]
        >>> map(lambda i: _SlicedPaginator(i, 6, 5).hidden_next_pages(), range(1, 7))
        [True, True, True, False, False, False]
        >>> map(lambda i: _SlicedPaginator(i, 7, 5).hidden_next_pages(), range(1, 8))
        [True, True, True, True, False, False, False]
        """
        next_pages = self.next_pages()
        return len(next_pages) > 0 and next_pages[-1] < self.npages


class _PaginatorSliceNode(Node):
    def __init__(self, context_name, paginatorname, maxpages_items):
        self.context_name = context_name
        self.paginatorname = paginatorname
        self.maxpages_items = maxpages_items
    def render(self, context):
        sliced_paginator = _SlicedPaginator(context[self.paginatorname].number,
                                            context[self.paginatorname].paginator.num_pages,
                                            self.maxpages_items)
        context[self.context_name] = sliced_paginator
        return ""
        

def _get_errstr(fnctn):
    s = "%s takes the syntax %s limited_pagination paginator_page max_items\
             as context_variable"
    return s % (fnctn, fnctn)

        
@register.tag
def sliced_pagination(parser, token):
    """
    Slices a paginator.
    
    Syntax:
    {% sliced_pagination page 5 as sliced_paginator %}
    
    where
     - page is an instance of the Django `Page` class.
     - max_items are the number of items to be shown in total. Ie., 5 will yield
        << 1 2 3 4 5 ... >>
       or
        << ... 4 5 6 7 8 ... >>
       or
        << ... 10 11 12 13 15 >>
       Currently only uneven numbers are supported for this parameter due to
       have even lists of pages on both sides.
    
    Sample syntax to use the sliced paginator:
    {% if sliced_paginator.hidden_prev_pages %}
    ...
    {% endif %}
    {% for pageno in sliced_paginator.prev_pages %}
        <a href="?page={{ pageno }}">{{ pageno}}</a>
    {% endfor %}
    <a href="#" class="current">{{ page.number }}</a>
    {% for pageno in sliced_paginator.next_pages %}
        <a href="?page={{ pageno }}">{{ pageno}}</a>
    {% endfor %}
    {% if sliced_paginator.hidden_next_pages %}
    ...
    {% endif %}
    
    Produces:
    ...           # only shown if needed
    <a href="?page=3">3</a>
    <a href="?page=4">4</a>
    <a href="#" class="current">5</a>
    <a href="?page=6">6</a>
    <a href="?page=7">7</a>
    ...           # only shown if needed
    
    """
    try:
        fnctn, paginatorname, max_items, trash, context_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, _get_errstr(fnctn)
    if not trash == 'as':
        raise TemplateSyntaxError, _get_errstr(fnctn)
    return _PaginatorSliceNode(context_name, paginatorname, max_items)