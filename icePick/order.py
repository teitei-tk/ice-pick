import enum
from .parser import Parser

__all__ = ('Order')


class Order:
    recorder = None
    parser = None

    class Method(enum.Enum):
        GET = "GET"
        POST = "POST"
        PUT = "POST"
        DELETE = "POST"

    def __init__(self, url, ua, method=None, charset='utf-8', content_type='text/html'):
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
        if not self.recorder:
            return False

        record = self.recorder.new(result)
        return record.save()
