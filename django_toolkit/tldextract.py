from __future__ import absolute_import
import os
import tldextract
from django.conf import settings

cached_tldextract = tldextract.TLDExtract(cache_file=os.path.join(settings.MEDIA_ROOT, 'tldextract', 'effective_tld_names.dat'))