import unittest
from nose.tools import ok_, eq_

import datetime
from pymongo import MongoClient

from tests.config import DB_HOST, DB_PORT, DB_NAME
from icePick.record import get_database, Structure, Record


db = get_database(DB_NAME, DB_HOST, DB_PORT)


class TestStructureModel(Structure):
    pass


class TestRecordModel(Record):
    struct = TestStructureModel(
        string=str(),
        intger=int(),
        boolean=bool(),
        list_=list(),
        dictionary=dict(),
        dt=datetime.datetime.now()
    )

    class Meta:
        database = db


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = TestRecordModel.new()

    def tearDown(self):
        m = MongoClient(DB_HOST, DB_PORT)
        m.drop_database(DB_NAME)

    def test_colname(self):
        eq_('test_record_model', self.record.colname())

    def test_attrs(self):
        new_str = "test_setattr"
        self.record.string = new_str

        eq_(new_str, self.record.string)

    def test_new(self):
        eq_(None, self.record.key())

        new_record = TestRecordModel.new({
            "string": "new_string"
        })
        eq_("new_string", new_record.string)

    def test_insert(self):
        eq_(None, self.record.key())

        self.record.string = "new_str"
        self.record.insert()

        eq_("new_str", self.record.string)
        self.assertNotEqual(None, self.record.key())

    def test_update(self):
        self.record.insert()
        self.assertNotEqual(None, self.record.key())

        self.record.string = "new_str"
        self.record.update()
        eq_("new_str", self.record.string)

    def test_save(self):
        self.record.string = "new_str"
        self.record.save()

        self.assertNotEqual(None, self.record.key())
        eq_("new_str", self.record.string)

        self.record.string = "update"
        self.record.save()
        eq_("update", self.record.string)

    def test_get(self):
        self.record.string = "new_str"
        self.record.save()

        exist_record = TestRecordModel.get(self.record.key())
        eq_(exist_record.key(), self.record.key())
        eq_(exist_record.string, self.record.string)

    def test_find(self):
        result = TestRecordModel.find()
        eq_(0, result.__len__())
        self.record.save()

        result = TestRecordModel.find()
        eq_(1, result.__len__())
        eq_(result[0].key(), self.record.key())

    def test_delete(self):
        self.record.save()

        result = TestRecordModel.find()
        eq_(1, result.__len__())

        self.record.delete()

        result = TestRecordModel.find()
        eq_(0, result.__len__())
