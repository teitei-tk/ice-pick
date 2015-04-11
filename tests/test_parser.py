import unittest
from nose.tools import ok_

import icePick
from tests.config import PARSE_HTML


class TestParserModel(icePick.Parser):
    def serialize(self):
        title = self.bs.find('title').text
        charset = self.bs.find('meta').get('charset')
        text = self.bs.find('p').text

        return {
            "title": title,
            "charset": charset,
            "text": text,
        }


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = TestParserModel(PARSE_HTML)

    def test_lang(self):
        ok_('en', self.parser.lang)

    def test_serialize(self):
        result = self.parser.serialize()

        ok_('TestHTML', result['title'])
        ok_('charset', result['charset'])
        ok_('HTML parse test', result['text'])

    def test_run(self):
        result = self.parser.run()

        ok_('TestHTML', result['title'])
        ok_('charset', result['charset'])
        ok_('HTML parse test', result['text'])
