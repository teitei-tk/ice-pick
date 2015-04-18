import unittest
from nose.tools import eq_
from pymongo import MongoClient

import icePick
from tests.config import DB_HOST, DB_PORT, DB_NAME, ORDER_URL, ORDER_UA


db = icePick.get_database(DB_NAME, DB_HOST, DB_PORT)


class TestParserModel(icePick.Parser):
    def serialize(self):
        result = {
            "files": [],
        }

        for v in self.bs.find_all(class_="js-directory-link"):
            result['files'] += [v.text]
        return result


class TestRecordModel(icePick.Record):
    struct = icePick.Structure(files=list())

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

    def tearDown(self):
        m = MongoClient(DB_HOST, DB_PORT)
        m.drop_database(DB_NAME)

    def test_run(self):
        self.picker.run()

        result = TestRecordModel.find()
        eq_(1, result.__len__())

        record = result[0]
        eq_('example', record.files[0])
        eq_('icePick', record.files[1])
        eq_('tests', record.files[2])
        eq_('LICENSE', record.files[3])
        eq_('README.md', record.files[4])
        eq_('requirements.txt', record.files[5])
