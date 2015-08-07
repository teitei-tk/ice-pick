import unittest
from nose.tools import eq_

from pymongo import MongoClient

import icePick
from tests.config import ORDER_URL, ORDER_UA, PARSE_HTML, DB_HOST, DB_PORT, DB_NAME

db = icePick.get_database(DB_NAME, DB_HOST, DB_PORT)


class TestOrderModel(icePick.Order):
    pass


class TestMultipleRecorder(icePick.Recorder):
    struct = icePick.Structure(exists_check=int(), value=str())

    class Meta:
        database = db


class TestMultipleOrderModel(icePick.Order):
    recorder = TestMultipleRecorder
    exists_keys = ["exists_check"]


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
        eq_(False, self.order.save({"exists_check": 1, "foo": "bar"}))

    def test_multi_save(self):
        values = [
            {"exists_check": 1, "value": "hoge"},
            {"exists_check": 2, "value": "fuga"},
        ]

        result = TestMultipleOrderModel(ORDER_URL, ORDER_UA).save(values)
        eq_(True, result)

        results = TestMultipleRecorder.find()
        eq_(values.__len__(), results.__len__())

        values = [
            {"exists_check": 1, "value": "bar"},
            {"exists_check": 3, "value": "piyo"},
        ]

        TestMultipleOrderModel(ORDER_URL, ORDER_UA).save(values)
        results = TestMultipleRecorder.find()
        eq_(3, results.__len__())
        eq_([1, 2, 3], [x.exists_check for x in results])
        eq_(["hoge", "fuga", "piyo"], [x.value for x in results])
