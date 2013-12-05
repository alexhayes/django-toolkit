from bs4 import BeautifulSoup

def get_anchor_href(markup):
    """
    Given HTML markup, return a list of hrefs for each anchor tag.
    """
    soup = BeautifulSoup(markup, 'lxml')
    return ['%s' % link.get('href') for link in soup.find_all('a')]

def get_anchor_contents(markup):
    """
    Given HTML markup, return a list of href inner html for each anchor tag.
    """
    soup = BeautifulSoup(markup, 'lxml')
    return ['%s' % link.contents[0] for link in soup.find_all('a')]