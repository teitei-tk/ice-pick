import unittest
from nose.tools import eq_
from pymongo import MongoClient
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler

import icePick
from tests.config import DB_HOST, DB_PORT, DB_NAME, ORDER_HOST, ORDER_PORT, ORDER_URL, ORDER_UA, PARSE_HTML
from tests.test_parser import TestParserModel as _TestParserModel

db = icePick.get_database(DB_NAME, DB_HOST, DB_PORT)


class TestRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        body = str.encode(PARSE_HTML)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)


class TestParserModel(_TestParserModel):
    pass


class TestRecordModel(icePick.Record):
    struct = icePick.Structure(title=str(), charset=str(), text=str())

    class Meta:
        database = db


class TestOrderModel(icePick.Order):
    def parse(self, html):
        parser = TestParserModel(html)
        return parser.run()

    def save(self, result):
        record = TestRecordModel.new(result)
        return record.save()


class TestPickerModel(unittest.TestCase):
    def setUp(self):
        order = TestOrderModel(ORDER_URL, ORDER_UA)
        self.picker = icePick.Picker([order])

        self.httpd = HTTPServer((ORDER_HOST, int(ORDER_PORT)), TestRequestHandler)

        thread = Thread(target=self.httpd.serve_forever)
        thread.start()

    def tearDown(self):
        thread = Thread(target=self.httpd.shutdown)
        thread.start()

        m = MongoClient(DB_HOST, DB_PORT)
        m.drop_database(DB_NAME)

    def test_run(self):
        result = TestRecordModel.find()
        eq_(0, result.__len__())

        self.picker.run()

        result = TestRecordModel.find()
        eq_(1, result.__len__())

        record = result[0]
        eq_('TestHTML', record.title)
        eq_('utf-8', record.charset)
        eq_('HTML parse test', record.text)
