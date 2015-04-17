import unittest
from nose.tools import eq_

import icePick
from tests.config import ORDER_URL, ORDER_UA, PARSE_HTML


class TestOrderModel(icePick.Order):
    pass


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order = TestOrderModel(ORDER_URL, ORDER_UA, method=TestOrderModel.Method.POST)

    def test_validate(self):
        eq_('utf-8', self.order.charset)
        eq_('text/html', self.order.content_type)
        eq_(icePick.Order.Method.POST, self.order.method)

        new_order = TestOrderModel(ORDER_URL, ORDER_UA, method="hogefuga", charset='uTF-8', content_type="TEXT/html")
        eq_('utf-8', new_order.charset)
        eq_('text/html', new_order.content_type)
        eq_(icePick.Order.Method.GET, new_order.method)

    def test_user_agent(self):
        eq_(ORDER_UA, self.order.user_agent)

    def test_get_headers(self):
        headers = {
            'User-agent': ORDER_UA,
            'Content-Type': "text/html; utf-8"
        }
        eq_(headers, self.order.get_headers())

    def test_parse(self):
        eq_({}, self.order.parse(PARSE_HTML))

    def test_save(self):
        eq_(None, self.order.save({"foo": "bar"}))
