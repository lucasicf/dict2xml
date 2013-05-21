# -*- coding: utf-8 -*-

from unittest import TestCase
from dict2xml import dict2XML

class SuccessTest(TestCase):

    def _build_xml(self, lines, indent=True, utf8=False):
        xml_header = (utf8 and '<?xml version="1.0" encoding="utf-8"?>'
                            or '<?xml version="1.0" ?>')
        if indent:
            merged_lines = '\n'.join(lines)
            basestr = '%s\n%s\n'
        else:
            merged_lines = ''.join([line.strip() for line in lines])
            basestr = '%s%s'
        if utf8:
            merged_lines = merged_lines.encode('utf-8')
        return basestr % (xml_header, merged_lines)

    def test_1(self):
        """
        Empty dict.
        """
        dict_ = {'root': {}}
        expected_xml = ['<root/>']
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))

    def test_2(self):
        """
        Simple unordered dict (key/simple values).
        """
        dict_ = {'root': {
            'nothing': '',
            'foo': 'oof',
            'bar': 'rab',
            'foobar': 'raboof'
        }}
        expected_xml = [
            '<root>',
            '  <bar>rab</bar>',
            '  <foo>oof</foo>',
            '  <foobar>raboof</foobar>',
            '  <nothing></nothing>',
            '</root>',
        ]
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))

    def test_3(self):
        """
        Simple ordered dict (key/simple values).
        """
        dict_ = {'1__root': {
            '2__nothing': '',
            '4__foo': 'oof',
            '1__bar': 'rab',
            '3__foobar': 'raboof'
        }}
        expected_xml = [
            '<root>',
            '  <bar>rab</bar>',
            '  <nothing></nothing>',
            '  <foobar>raboof</foobar>',
            '  <foo>oof</foo>',
            '</root>',
        ]
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))

    def test_4(self):
        """
        Simple mixed-ordered dict (key/simple values).
        """
        dict_ = {'root': {
            '2__nothing': '',
            'foo': 'oof',
            'bar': 'rab',
            '3__foobar': 'raboof'
        }}
        expected_xml = [
            '<root>',
            '  <nothing></nothing>',
            '  <foobar>raboof</foobar>',
            '  <bar>rab</bar>',
            '  <foo>oof</foo>',
            '</root>',
        ]
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))

    def test_5(self):
        """
        Simple ordered dict (key/simple values) encoded with utf-8.
        """
        dict_ = {u'ròót': {
            '2__nothing': '',
            u'4__fôó': 'oof',
            '1__bar': u'ráb',
            u'3__fõôbár': u'rábôõf'
        }}
        expected_xml = [
            u'<ròót>',
            u'  <bar>ráb</bar>',
            u'  <nothing></nothing>',
            u'  <fõôbár>rábôõf</fõôbár>',
            u'  <fôó>oof</fôó>',
            u'</ròót>',
        ]
        self.assertEqual(dict2XML(dict_, utf8=True), self._build_xml(expected_xml, utf8=True))
        self.assertEqual(dict2XML(dict_, indent=False, utf8=True),
                         self._build_xml(expected_xml, indent=False, utf8=True))

    def test_6(self):
        """
        Ordered dict with nested dicts.
        """
        dict_ = {'root': {
            '1__bar': 'rab',
            '2__nothing': '',
            '3__subdict': {
                '1__anothersubdict': {
                    'hey': 'ya'
                },
                '2__foobar': 'raboof'
            },
            '4__emptysubdict': {},
            '5__foo': 'oof',
        }}
        expected_xml = [
            '<root>',
            '  <bar>rab</bar>',
            '  <nothing></nothing>',
            '  <subdict>',
            '    <anothersubdict>',
            '      <hey>ya</hey>',
            '    </anothersubdict>',
            '    <foobar>raboof</foobar>',
            '  </subdict>',
            '  <emptysubdict/>',
            '  <foo>oof</foo>',
            '</root>',
        ]
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))

    def test_7(self):
        """
        Ordered dict with nested dicts and lists.
        """
        dict_ = {'root': {
            '1__list': [
                '1',
                {
                    'foo': ['bar']
                },
                {
                    '1__foo': {
                        '1__a': '1',
                        '2__b': ['2', '3', '4']
                    },
                    '2__bar': [
                        {
                          'foo': 'bar'
                        },
                        ''
                    ],
                },
                '2'
            ],
            '2__nothing': {}
        }}
        expected_xml = [
            '<root>',
            '  <list>1</list>',
            '  <list>',
            '    <foo>bar</foo>',
            '  </list>',
            '  <list>',
            '    <foo>',
            '      <a>1</a>',
            '      <b>2</b>',
            '      <b>3</b>',
            '      <b>4</b>',
            '    </foo>',
            '    <bar>',
            '      <foo>bar</foo>',
            '    </bar>',
            '    <bar></bar>',
            '  </list>',
            '  <list>2</list>',
            '  <nothing/>',
            '</root>',
        ]
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))

    def test_8(self):
        """
        Ordered dict with nested dicts and lists and element attributes
        """
        dict_ = {'root': ({'a': 'b'}, {
            '1__list': [
                '1',
                {
                    'foo': ['bar']
                },
                {
                    '1__foo': ({'c': 'd', 'e': 'f'}, {
                        '1__a': '1',
                        '2__b': [
                            ({'A': 'B', 'C': 'D'}, '2'),
                            '3',
                            ({'E': 'F'}, '4')
                        ]
                    }),
                    '2__bar': [
                        {
                          'foo': ({'g': 'h', 'i': 'j'}, 'bar')
                        },
                        ''
                    ],
                },
                '2'
            ],
            '2__nothing': {}
        })}
        expected_xml = [
            '<root a="b">',
            '  <list>1</list>',
            '  <list>',
            '    <foo>bar</foo>',
            '  </list>',
            '  <list>',
            '    <foo c="d" e="f">',
            '      <a>1</a>',
            '      <b A="B" C="D">2</b>',
            '      <b>3</b>',
            '      <b E="F">4</b>',
            '    </foo>',
            '    <bar>',
            '      <foo g="h" i="j">bar</foo>',
            '    </bar>',
            '    <bar></bar>',
            '  </list>',
            '  <list>2</list>',
            '  <nothing/>',
            '</root>',
        ]
        self.assertEqual(dict2XML(dict_), self._build_xml(expected_xml))
        self.assertEqual(dict2XML(dict_, indent=False),
                         self._build_xml(expected_xml, indent=False))
