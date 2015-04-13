import re
import datetime
from pymongo import MongoClient
from .exception import RecordException, StructureException

__all__ = ('get_database', 'Record', 'Structure')


def get_database(db_name, host, port=27017):
    return MongoClient(host, port)[db_name]


class Structure(dict):
    __store = {}

    def __init__(self, *args, **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def init_from_dict(self, data):
        if not isinstance(data, dict):
            data = {}

        # initialize store
        self.__store = {}

        for key, value in self.__dict__.items():
            result = data.get(key)
            if not result:
                result = value
            self.__store[key] = value

        self._validate()

    def _validate(self):
        pass

    def assign_to_store(self, key, value):
        if key in self.__store.keys():
            self.__store[key] = value
            return True
        raise StructureException("value is invalid type, key : {0}".format(value))

    def get_from_store(self, key):
        if key in self.__store.keys():
            return self.__store[key]
        raise StructureException("{0} is not a registered".format(key))

    def to_dict(self):
        return self.__store

    def to_mongo(self):
        store = self.to_dict()

        now = datetime.datetime.now()
        if not 'created_at' in store.keys():
            store['created_at'] = now
        store['modified_at'] = now
        return store


class Record:
    struct = None

    class Meta:
        database = None

    def __init__(self, key, data=None):
        self._key = key
        self._init_from_dict(data)

    def _init_from_dict(self, data):
        if not isinstance(self.struct, Structure):
            raise RecordException("{0} struct is not a defined".format(self.__class__.__name__))

        # initialize store data
        self.struct.init_from_dict(data)

    def key(self):
        return self._key

    def __str__(self):
        return self.__name__

    def __getattr__(self, key):
        return self.struct.get_from_store(key)

    def __setattr__(self, key, value):
        if key in self.struct.keys():
            self.struct.assign_to_store(key, value)
        else:
            super(Record, self).__setattr__(key, value)

    @classmethod
    def colname(cls):
        return re.sub('(?!^)([A-Z]+)', r'_\1', cls.__name__).lower().__str__()

    @classmethod
    def collection(cls):
        return cls.Meta.database[cls.colname()]

    @classmethod
    def new(cls):
        return cls(None)

    @classmethod
    def get(cls, key, *args, **kwargs):
        data = cls.collection().find_one(query={"_id": key}, *args, **kwargs)
        if not data:
            return None
        return cls(key, data)

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.collection().find(*args, **kwargs)

    def save(self):
        if not self.key():
            return self.insert()
        return self.update({'_id': self.key()})

    def insert(self):
        result = self.collection().insert_one(self.struct.to_mongo())

        self._key = result.inserted_id
        self.struct.assign_to_store('_id', result.inserted_id)
        return True

    def update(self, query, upsert=False):
        self.collection().update_one(query, self.struct.to_mongo(), upsert=upsert)
        return True

    def delete(self, query):
        self.collection().delete_one(query)
        return True
