from django_toolkit.tldextract import cached_tldextract

def shorten_url(url, length=32, strip_www=True):
    """
    Shorten a URL by chopping out the middle.
    
    For example if supplied with http://subdomain.example.com.au and length 16
    the following would be returned.
    
    sub...le.com.au
    """
    ext = cached_tldextract(url)
    if ext.subdomain and (strip_www == False or (strip_www and ext.subdomain != 'www')):
        url = '%s.%s.%s' % (ext.subdomain, ext.domain, ext.tld)
    else:
        url = '%s.%s' % (ext.domain, ext.tld)
    
    if len(url) <= length:
        return url
    else:
        if ext.subdomain and (strip_www == False or (strip_www and ext.subdomain != 'www')):
            domain = '%s.%s' % (ext.subdomain, ext.domain)
        else:
            domain = ext.domain
        i = length - 3 - len(ext.tld) #23
        y = i/2  #3
        left = right = i/2
        if not i % 2:
            right -= 1
        domain = '%s...%s' % (domain[:left], domain[-right:])
        return '%s.%s' % (domain, ext.tld)

def netloc_no_www(url):
    """
    For a given URL return the netloc with any www. striped.
    """
    ext = cached_tldextract(url)
    if ext.subdomain and ext.subdomain != 'www':
        return '%s.%s.%s' % (ext.subdomain, ext.domain, ext.tld) 
    else:
        return '%s.%s' % (ext.domain, ext.tld)