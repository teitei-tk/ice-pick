import unittest
from nose.tools import ok_

import datetime

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
        pass
