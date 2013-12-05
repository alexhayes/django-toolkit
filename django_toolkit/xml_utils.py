from xml.etree import ElementTree
from xml.dom.ext import PrettyPrint
from cStringIO import StringIO
from xml.dom.minidom import parseString

def prettify(root, encoding='utf-8'):
    """
    Return a pretty-printed XML string for the Element.
    
    @see: http://www.doughellmann.com/PyMOTW/xml/etree/ElementTree/create.html
    """
    if isinstance(root, ElementTree.Element):
        node = ElementTree.tostring(root, 'utf-8')
    else:
        node = root
    tmpStream = StringIO()
    PrettyPrint(parseString(node), stream=tmpStream, encoding=encoding)
    return tmpStream.getvalue()