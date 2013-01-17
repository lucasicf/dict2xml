# -*- coding: utf-8 -*-

from xml.dom import minidom
import re

# Thrown on any dictionary error
class Dict2XMLException(Exception):
    pass

def _dict_sort_key(key_value):
    key = key_value[0]
    match = re.match('(\d+)__.*', key)
    return int(match.groups()[0]) if match else key

_iter_dict_sorted = lambda dic: sorted(dic.iteritems(),
    key=lambda key_value: _dict_sort_key(key_value)
)

def _remove_order_id(key):
    match = re.match('\d+__(.*)', key)
    return match.groups()[0] if match else key

def _check_errors(value, dataType):
    if dataType == 'rootDict':
        if isinstance(value, dict):
            values = value.values()
            if len(values) != 1:
                raise Dict2XMLException(
                    'Must have exactly one root element in the dictionary.'
                )
            elif isinstance(values[0], list):
                raise Dict2XMLException(
                    'The root element of the dictionary cannot '
                    'have a list as value.'
                )
        else:
            raise Dict2XMLException(
                'Must pass a dictionary as an argument.'
            )

    elif dataType == 'key':
        if not isinstance(value, str):
            raise Dict2XMLException('A key must be a string.')

    elif dataType == 'attr':
        (attr, attrValue) = value
        if not isinstance(attr, str):
            raise Dict2XMLException('An attribute key must be a string.')
        if not isinstance(attrValue, basestring):
            raise Dict2XMLException('An attribute value must be a string.')

    elif dataType == 'attrs':
        if not isinstance(value, dict):
            raise Dict2XMLException(
                'The first element of tuple must be a dictionary '
                'with a set of attributes for this element.'
            )

# Recursive core function
def _buildXMLTree(rootXMLElement, key, content, document):
    _check_errors(key, 'key')
    keyElement = document.createElement(_remove_order_id(key))

    (attrs, value) = (content
                        if (isinstance(content, tuple)
                                and len(content) == 2
                        ) else
                            ({}, content)
    )

    _check_errors(attrs, 'attrs')
    for (attr, attrValue) in attrs.iteritems():
        _check_errors((attr, attrValue), 'attr')
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
        raise Dict2XMLException('A key value must be:\n'
            '  1. A string;\n'
            '  2. A dictionary;\n'
            '  3. A tuple containing the attributes\' '
            'dictionary and the actual value;\n'
            '  4. A list of values with one of those types '
            'except the tuple.'
        )
def dict2XML(dic, indent=True, utf8=False):
    document = minidom.Document()

    # Root call of the recursion
    _check_errors(dic, 'rootDict')
    (key, content) = dic.items()[0]
    _buildXMLTree(document, key, content, document)

    return (document.toprettyxml(
                indent='  ', encoding=('utf-8' if utf8 else None)
            ) if indent else
                    document.toxml(encoding=('utf-8' if utf8 else None))
    )
