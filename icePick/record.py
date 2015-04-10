import re
from .exception import RecordException, StructureException

__all__ = ('Record', 'Structure')


class Structure(dict):
    __store = {}

    def __init__(self, *args, **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def init_from_dict(self, data):
        if not isinstance(data, dict):
            raise StructureException("%s arg is not a dictionary" % self.__class__.__name__)

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
        raise StructureException("value is invalid type, key : {0}".format(value))

    def get_from_store(self, key):
        if key in self.__store.keys():
            return self.__store[key]
        raise StructureException("{0} is not a registered".format(key))

    def to_dict(self):
        return self.__store


class Record:
    struct = None

    class Meta:
        database = None

    def __init__(self, key, data=None):
        self._key = key
        self.init_from_dict(data)

    def init_from_dict(self, data):
        if not isinstance(self.struct, Structure):
            raise RecordException("%s struct is not a defined" % self.__class__.__name__)

        # initialize store data
        self.struct.init_from_dict(data)

    def key(self):
        return self._key

    def __str__(self):
        return self.__class__.__name__

    def __getattr__(self, key):
        return self.struct.get_from_store(key)

    def __setattr__(self, key, value):
        self.struct.assign_for_store(key, value)

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
    def find(cls, *args, **kwargs):
        return cls.collection().find(*args, **kwargs)

    def save(self):
        if not self.key():
            return self.insert()
        return self.update({'_id': self.key()})

    def insert(self):
        result = self.collection().insert_one(self.struct.to_dict())
        self.__store["_id"] = result.inserted_id
        self._key = result.inserted_id
        return True

    def update(self, query, upsert=False):
        self.collection().update_one(query, self.struct.to_dict(), upsert=upsert)
        return True

    def delete(self, query):
        self.collection().delete_one(query)
        return True
