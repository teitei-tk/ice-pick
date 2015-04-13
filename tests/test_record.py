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
