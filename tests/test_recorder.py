import unittest
from nose.tools import ok_, eq_

import datetime
from pymongo import MongoClient

from tests.config import DB_HOST, DB_PORT, DB_NAME
from icePick.recorder import get_database, Structure, Recorder


db = get_database(DB_NAME, DB_HOST, DB_PORT)


class TestStructureModel(Structure):
    pass


class TestRecorderModel(Recorder):
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


class TestRecorder(unittest.TestCase):
    def setUp(self):
        self.record = TestRecorderModel.new()

    def tearDown(self):
        m = MongoClient(DB_HOST, DB_PORT)
        m.drop_database(DB_NAME)

    def test_colname(self):
        eq_('test_recorder_model', self.record.colname())

    def test_attrs(self):
        new_str = "test_setattr"
        self.record.string = new_str

        eq_(new_str, self.record.string)

    def test_new(self):
        eq_(None, self.record.key())

        new_record = TestRecorderModel.new({
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

        exist_record = TestRecorderModel.get(self.record.key())
        eq_(exist_record.key(), self.record.key())
        eq_(exist_record.string, self.record.string)

    def test_find(self):
        result = TestRecorderModel.find()
        eq_(0, result.count())
        self.record.save()

        result = TestRecorderModel.find()
        eq_(1, result.count())

        entity = TestRecorderModel.create(result[0])
        eq_(entity.key(), self.record.key())

    def test_delete(self):
        self.record.save()

        result = TestRecorderModel.find()
        eq_(1, result.count())

        self.record.delete()

        result = TestRecorderModel.find()
        eq_(0, result.count())
