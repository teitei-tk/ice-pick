import enum
from .parser import Parser

__all__ = ('Order')


class Order:
    class Method(enum.Enum):
        GET = "GET"
        POST = "POST"
        PUT = "POST"
        DELETE = "POST"

    def __init__(self, url, ua, method=None, charset='utf-8', content_type='text/html'):
        self.url = url
        self.ua = ua
        self.method = method
        self.charset = charset
        self.content_type = content_type

        self._validate()

    def _validate(self):
        self.charset = self.charset.lower()
        self.content_type = self.content_type.lower()

        if not isinstance(self.method, self.Method):
            self.method = self.Method.GET

    @property
    def user_agent(self):
        return self.ua

    def get_headers(self):
        headers = {
            'User-agent': self.user_agent,
            'Content-Type': "{0}; {1}".format(self.content_type, self.charset)
        }
        return headers

    def parse(self, html):
        """
        parser = Parser(html)
        return parser.run()
        """
        return {}

    def save(self, result):
        """
        record = Record.new()
        record.save(result)
        """
        pass
