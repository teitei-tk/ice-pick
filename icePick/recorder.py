import re
import datetime
from pymongo import MongoClient
from bson import ObjectId
from .exception import RecorderException, StructureException

__all__ = ['get_database', 'Recorder', 'Structure']


def get_database(db_name, host, port=27017):
    return MongoClient(host, port)[db_name]


class Structure(dict):
    __store = {}

    def __init__(self, *args, **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self._validate()

    def _validate(self):
        pass

    def to_dict(self):
        return self.__dict__


class Recorder:
    struct = None
    __store = None

    class Meta:
        database = None

    class DataStore:
        def get(self, key):
            return self.__dict__.get(key)

        def set(self, key, value):
            self.__dict__[key] = value

        def to_dict(self):
            return self.__dict__

    def __init__(self, key, data=None):
        self._key = key
        self.__store = self.DataStore()

        self._init_from_dict(data)

    def _init_from_dict(self, data):
        if not isinstance(self.struct, Structure):
            raise RecorderException("{0} struct is not a defined".format(self.__class__.__name__))

        if not isinstance(data, dict):
            data = dict()

        # initialize store data
        for k, v in self.struct.to_dict().items():
            result = data.get(k)
            if not result:
                result = v
            self.__store.set(k, result)

    def key(self):
        return self._key

    def pk(self):
        return ObjectId(self.key())

    def __str__(self):
        return self.__name__

    def __getattr__(self, key):
        if key in list(self.struct.keys()):
            return self.__store.get(key)
        else:
            return super(Recorder, self).__getattr__(key)

    def __setattr__(self, key, value):
        if key in list(self.struct.keys()):
            self.__store.set(key, value)
        else:
            super(Recorder, self).__setattr__(key, value)

    @classmethod
    def colname(cls):
        return re.sub('(?!^)([A-Z]+)', r'_\1', cls.__name__).lower().__str__()

    @classmethod
    def collection(cls):
        return cls.Meta.database[cls.colname()]

    @classmethod
    def new(cls, data=None):
        return cls(None, data)

    @classmethod
    def create(cls, data):
        key = None
        if '_id' in data.keys():
            key = data['_id']
            if isinstance(data['_id'], ObjectId):
                key = data['_id'].__str__()

        return cls(key, data)

    @classmethod
    def get(cls, key, *args, **kwargs):
        data = cls.collection().find_one({'_id': ObjectId(key)}, *args, **kwargs)
        if not data:
            return None
        return cls(key, data)

    @classmethod
    def get_by(cls, key, value, *args, **kwargs):
        data = cls.collection().find_one({key: value}, *args, **kwargs)
        if not data:
            return None
        return cls.create(data)

    @classmethod
    def find(cls, *args, **kwargs):
        return [cls.create(x) for x in cls.collection().find(*args, **kwargs)]

    def save(self):
        if not self.key():
            return self.insert()
        return self.update()

    def insert(self):
        result = self.collection().insert_one(self.to_mongo())

        self._key = result.inserted_id.__str__()
        self.__store.set('_id', self.key())
        return True

    def update(self, upsert=False):
        if not self.key():
            return self.insert()

        self.collection().update_one({'_id': self.pk()}, {'$set': self.to_mongo()}, upsert=upsert)
        return True

    def delete(self):
        if not self.key():
            return False

        self.collection().delete_one({'_id': self.pk()})
        return True

    @classmethod
    def exists(cls, key, value):
        return cls.find(filter={key: value}, limit=1).__len__() > 0

    def to_dict(self):
        return self.__store.to_dict()

    def to_mongo(self):
        store = self.to_dict()

        now = datetime.datetime.now()
        if not 'created_at' in store.keys():
            store['created_at'] = now
        store['modified_at'] = now

        if '_id' in store.keys():
            del store['_id']
        return store
