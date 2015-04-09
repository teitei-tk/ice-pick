from .parser import Parser


class Order:
    def __init__(self, url, ua, method='GET', charset='utf-8', content_type='text/html'):
        self.url = url
        self.ua = ua
        self.method = method
        self.charset = charset
        self.content_type = content_type

    @property
    def user_agent(self):
        return self.ua

    def get_headers(self):
        headers = {
            'User-agent': self.user_agent,
            'Content-Type': "%s; %s" % (self.content_type, self.charset)
        }
        return headers

    def to_dict(self, html):
        """
        parser = Parser(html)
        return parser.run()
        """
        return {}

    def save(self, result):
        """
        record = Record.create()
        record.save(result)
        """
        pass
