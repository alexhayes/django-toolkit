from xml.etree import ElementTree
from cStringIO import StringIO
from xml.dom.minidom import parseString
from lxml import etree


def prettify(root, encoding='utf-8'):
    """
    Return a pretty-printed XML string for the Element.

    @see: http://www.doughellmann.com/PyMOTW/xml/etree/ElementTree/create.html
    """
    if isinstance(root, ElementTree.Element):
        node = ElementTree.tostring(root, 'utf-8')
    else:
        node = root

    # Hacky solution as it seems PyXML doesn't exist anymore... 
    return etree.tostring(etree.fromstring(node),
                          pretty_print=True,
                          xml_declaration=True,
                          encoding='utf-8')
