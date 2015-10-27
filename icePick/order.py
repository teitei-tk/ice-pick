import enum

from .parser import Parser
from .recorder import Recorder

__all__ = ('Order')


class Order:
    recorder = None
    parser = None
    exists_keys = []

    class Method(enum.Enum):
        GET = "GET"
        POST = "POST"
        PUT = "POST"
        DELETE = "POST"

    class UserAgent(enum.Enum):
        IE = "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
        FIRE_FOX = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0"
        CHROME = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"

    def __init__(self, url, ua=None, method=None, charset='utf-8', content_type='text/html'):
        self.url = url
        self.user_agent = ua
        self.method = method
        self.charset = charset
        self.content_type = content_type

        self._validate()

    def _validate(self):
        self.charset = self.charset.lower()
        self.content_type = self.content_type.lower()

        if not isinstance(self.method, self.Method):
            self.method = self.Method.GET

        if self.user_agent is None:
            self.user_agent = self.UserAgent.IE.value

    def get_headers(self):
        headers = {
            'User-agent': self.user_agent,
            'Content-Type': "{0}; {1}".format(self.content_type, self.charset)
        }
        return headers

    def parse(self, html):
        if not self.parser:
            return {}

        parser = self.parser(html)
        return parser.run()

    def save(self, result):
        def get_entity(value):
            if self.exists_keys.__len__() <= 0:
                return self.recorder.new(value)

            for key in self.exists_keys:
                record = self.recorder.get_by(key, value.get(key))
                if not record:
                    continue
                return record
            return self.recorder.new(value)

        if self.recorder is None:
            return False

        if isinstance(result, list):
            return list(filter(lambda x: get_entity(x).save(), result)).__len__() <= result.__len__()

        elif isinstance(result, dict):
            return get_entity(result).save()

        return False
