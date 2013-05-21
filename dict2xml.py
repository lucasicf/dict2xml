# -*- coding: utf-8 -*-

from xml.dom import minidom
import re

# Thrown on any dictionary error
class Dict2XMLException(Exception):
    pass

def _dict_sort_key(key_value):
    key = key_value[0]
    match = re.match('(\d+)__.*', key)
    return match and int(match.groups()[0]) or key

_iter_dict_sorted = lambda dic: sorted(
    dic.iteritems(), key=(lambda key_value: _dict_sort_key(key_value))
)

def _remove_order_id(key):
    match = re.match('\d+__(.*)', key)
    return match and match.groups()[0] or key

DATATYPE_ROOT_DICT = 0
DATATYPE_KEY = 1
DATATYPE_ATTR = 2
DATATYPE_ATTRS = 3

def _check_errors(value, data_type):
    if data_type == DATATYPE_ROOT_DICT:
        if isinstance(value, dict):
            values = value.values()
            if len(values) != 1:
                raise Dict2XMLException(
                    'Must have exactly one root element in the dictionary.')
            elif isinstance(values[0], list):
                raise Dict2XMLException(
                    'The root element of the dictionary cannot have a list as value.')
        else:
            raise Dict2XMLException('Must pass a dictionary as an argument.')

    elif data_type == DATATYPE_KEY:
        if not isinstance(value, basestring):
            raise Dict2XMLException('A key must be a string.')

    elif data_type == DATATYPE_ATTR:
        (attr, attrValue) = value
        if not isinstance(attr, basestring):
            raise Dict2XMLException('An attribute\'s key must be a string.')
        if not isinstance(attrValue, basestring):
            raise Dict2XMLException('An attribute\'s value must be a string.')

    elif data_type == DATATYPE_ATTRS:
        if not isinstance(value, dict):
            raise Dict2XMLException('The first element of a tuple must be a dictionary '
                                    'with a set of attributes for the main element.')

# Recursive core function
def _buildXMLTree(rootXMLElement, key, content, document):
    _check_errors(key, DATATYPE_KEY)
    keyElement = document.createElement(_remove_order_id(key))

    if isinstance(content, tuple) and len(content) == 2:
        (attrs, value) = content
    else:
        (attrs, value) = ({}, content)

    _check_errors(attrs, DATATYPE_ATTRS)
    for (attr, attrValue) in attrs.iteritems():
        _check_errors((attr, attrValue), DATATYPE_ATTR)
        keyElement.setAttribute(attr, '%s' % attrValue)

    if isinstance(value, basestring):
        # Simple text value inside the node
        keyElement.appendChild(document.createTextNode('%s' % value))
        rootXMLElement.appendChild(keyElement)

    elif isinstance(value, dict):
        # Iterating over the children
        for (k, cont) in _iter_dict_sorted(value):
            # Recursively parse the subdictionaries
            _buildXMLTree(keyElement, k, cont, document)
        rootXMLElement.appendChild(keyElement)

    elif isinstance(value, list):
        # Recursively replicate this key element for each value in the list
        for subcontent in value:
            _buildXMLTree(rootXMLElement, key, subcontent, document)

    else:
        raise Dict2XMLException('Invalid value.')

def dict2XML(dic, indent=True, utf8=False):
    document = minidom.Document()

    # Root call of the recursion
    _check_errors(dic, DATATYPE_ROOT_DICT)
    (key, content) = dic.items()[0]
    _buildXMLTree(document, key, content, document)

    encoding = utf8 and 'utf-8' or None
    return (indent and document.toprettyxml(indent='  ', encoding=encoding)
                    or document.toxml(encoding=encoding))
