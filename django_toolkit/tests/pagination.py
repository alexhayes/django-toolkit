import unittest
from django_toolkit.pagination import RangeBasedPaginator

class RangeBasedPaginatorTestCase(unittest.TestCase):
    
    def test_num_pages(self):
        self.assertEqual(RangeBasedPaginator(10, 5).num_pages, 2)
        self.assertEqual(RangeBasedPaginator(10, 1).num_pages, 10)
        self.assertEqual(RangeBasedPaginator(10, 10).num_pages, 1)
        self.assertEqual(RangeBasedPaginator(10, 20).num_pages, 1)
    
    def test_page_range(self):
        self.assertEqual(RangeBasedPaginator(10, 5).page_range, [1, 2])
        self.assertEqual(RangeBasedPaginator(10, 1).page_range, range(1, 11))
        self.assertEqual(RangeBasedPaginator(10, 10).page_range, [1])
        self.assertEqual(RangeBasedPaginator(10, 20).page_range, [1])
    
    def test_paging(self):
        paginator = RangeBasedPaginator(10, 5)
        page = paginator.page(1)
        self.assertEqual(page.start_index(), 1)
        self.assertEqual(page.end_index(), 5)
        
        page = paginator.page(2)
        self.assertEqual(page.start_index(), 6)
        self.assertEqual(page.end_index(), 10)
