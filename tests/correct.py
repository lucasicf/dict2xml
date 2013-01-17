#-*- coding:utf-8 -*-

from unittest import TestCase
from dict2xml import dict2XML

class CorrectTest(TestCase):

    def setUp(self):
        self.XML_HEADER = '<?xml version="1.0" ?>'
        self.XML_HEADER_UTF8 = '<?xml version="1.0" encoding="utf-8"?>'

    def test_1(self):
        self.assertEqual(dict2XML({'root': {}}),
                         '%s\n<root/>\n' % self.XML_HEADER)

        dic = {
            'root': ({'xmlns': 'www.kgapwgjkwapigja.com', '1': 'ok'}, {
                '1__foo': '2',
                '3__ok': {
                    '1__hey': {
                        '1__test': 'www.google.com',
                        '2__bar': '3.2',
                    },
                    '2__ok': ({'style': 'red'}, {
                        'nothing': 'nonono',
                    }),
                },
                '15__empty': {},
                '2__bar': ({'attr': 'test'},
                    '3'
                ),
            })
        }

        xml1 = (
            '%s\n'
            '<root 1="ok" xmlns="www.kgapwgjkwapigja.com">\n'
            '  <foo>2</foo>\n'
            '  <bar attr="test">3</bar>\n'
            '  <ok>\n'
            '    <hey>\n'
            '      <test>www.google.com</test>\n'
            '      <bar>3.2</bar>\n'
            '    </hey>\n'
            '    <ok style="red">\n'
            '      <nothing>nonono</nothing>\n'
            '    </ok>\n'
            '  </ok>\n'
            '  <empty/>\n'
            '</root>\n'
        ) % self.XML_HEADER

        xml2 = lambda utf8: (
            '%s'
            '<root 1="ok" xmlns="www.kgapwgjkwapigja.com">'
            '<foo>2</foo>'
            '<bar attr="test">3</bar>'
            '<ok>'
            '<hey>'
            '<test>www.google.com</test>'
            '<bar>3.2</bar>'
            '</hey>'
            '<ok style="red">'
            '<nothing>nonono</nothing>'
            '</ok>'
            '</ok>'
            '<empty/>'
            '</root>'
        ) % (self.XML_HEADER_UTF8 if utf8 else self.XML_HEADER)

        self.assertEqual(dict2XML(dic), xml1)
        self.assertEqual(dict2XML(dic, indent=False), xml2(False))
        self.assertEqual(dict2XML(dic, indent=False, utf8=True), xml2(True))

    def test_2(self):
        dic = lambda utf8: {
            'root': {
                '1__multiple': [
                    ({'A': 'B'}, {
                        'foo': u'bar' if utf8 else 'bar'
                    }),
                    {
                        'foo': {
                            'a': '2',
                            'nonAscii': (u'bár fôo Bár'
                                            if utf8 else
                                            'bár fôo Bár'),
                        }
                    },
                    '2'
                ],
                '2__nothing': {}
            }
        }
        def xml(utf8):
            result = (
                '%s'
                '<root>'
                '<multiple A="B">'
                '<foo>bar</foo>'
                '</multiple>'
                '<multiple>'
                '<foo>'
                '<a>2</a>' +
                (u'<nonAscii>bár fôo Bár</nonAscii>'
                    if utf8 else
                    '<nonAscii>bár fôo Bár</nonAscii>') +
                '</foo>'
                '</multiple>'
                '<multiple>2</multiple>'
                '<nothing/>'
                '</root>'
            )
            return ((result % self.XML_HEADER_UTF8).encode('utf-8')
                        if utf8 else
                        result % self.XML_HEADER)

        self.assertEqual(dict2XML(dic(False), indent=False),
                         xml(False))
        self.assertEqual(dict2XML(dic(True), indent=False, utf8=True),
                         xml(True))
