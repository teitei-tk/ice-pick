import unittest
from nose.tools import eq_

from pymongo import MongoClient

import icePick
from tests.config import ORDER_URL, ORDER_UA, PARSE_HTML, DB_HOST, DB_PORT, DB_NAME

db = icePick.get_database(DB_NAME, DB_HOST, DB_PORT)


class TestOrderModel(icePick.Order):
    pass


class TestMultipleRecorder(icePick.Recorder):
    struct = icePick.Structure(value=str())

    class Meta:
        database = db


class TestMultipleOrderModel(icePick.Order):
    recorder = TestMultipleRecorder


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order = TestOrderModel(ORDER_URL, ORDER_UA, method=TestOrderModel.Method.POST)

    def tearDown(self):
        m = MongoClient(DB_HOST, DB_PORT)
        m.drop_database(DB_NAME)

    def test_validate(self):
        eq_('utf-8', self.order.charset)
        eq_('text/html', self.order.content_type)
        eq_(icePick.Order.Method.POST, self.order.method)

        new_order = TestOrderModel(ORDER_URL, ORDER_UA, method="hogefuga", charset='uTF-8', content_type="TEXT/html")
        eq_('utf-8', new_order.charset)
        eq_('text/html', new_order.content_type)
        eq_(icePick.Order.Method.GET, new_order.method)

    def test_get_headers(self):
        headers = {
            'User-agent': ORDER_UA,
            'Content-Type': "text/html; utf-8"
        }
        eq_(headers, self.order.get_headers())

    def test_parse(self):
        eq_({}, self.order.parse(PARSE_HTML))

    def test_save(self):
        eq_(False, self.order.save({"foo": "bar"}))

    def test_multi_save(self):
        values = [
            {"value": "hoge"},
            {"value": "fuga"},
        ]

        order = TestMultipleOrderModel(ORDER_URL, ORDER_UA)
        result = order.save(values)
        eq_(True, result)

        result = TestMultipleRecorder.find()
        eq_(values.__len__(), result.count())
