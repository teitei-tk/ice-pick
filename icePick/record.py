import re
import hashlib
import datetime
from .icePick.exception import RecordException

__all = ('Record', 'Structure')


class Record:
    struct = None
    __store = {}

    class Meta:
        database = None

    def __init__(self, key, data=None):
        self._key = key

        self.init_from_dict(data)
        self._validate()

    def init_from_dict(self, data):
        if not self.struct or not isinstance(self.struct, dict) or self._struct.__len__() <= 0:
            raise RecordException("%s struct is not a defined" % self.__class__.__name__)

        # initialize store data
        self.__store = {}

        for key, value in self.struct.items():
            # TODO : TypeCheck
            result = data.get(key)
            if not result:
                result = value
            self.__store[key] = result

    def _validate(self):
        pass

    def key(self):
        return self._key

    def __str__(self):
        return self.__class__.__name__

    def __getattr__(self, key):
        # TODO : Error Pattern
        if key in self.__store:
            return self.__store[key]
        raise Exception()

    def __setattr__(self, key, value):
        # TODO : Error Pattern
        if key in self.__store.keys():
            # TODO : TypeCheck
            self.__store[key] = value
            return self.__store[key]
        raise Exception()

    @classmethod
    def colname(cls):
        return re.sub('(?!^)([A-Z]+)', r'_\1', cls.__class__.__name__).lower()

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
    def find(cls, **kwargs):
        return cls.collection().find(**kwargs)

    def insert(self):
        result = self.collection().insert_one(self.__store)
        self.__store["_id"] = result.inserted_id
        self._key = result.inserted_id
        return True

    def update(self, query, upsert=False):
        self.collection().update_one(query, self.__store, upsert=upsert)
        return True

    def delete(self, query):
        self.collection().delete_one(query)
        return True
