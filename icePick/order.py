from .parser import Parser


class Order:
    def __init__(self, url, ua, method='GET', content_type='text/html', charset='utf-8'):
        self.url = url
        self.ua = ua
        self.method = method
        self.content_type = content_type
        self.charset = charset

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
        parser = Parser(html)
        parser.run()

        return {}

    def save(self, result):
        """
        hoge = Record.create()
        hoge.save(result)
        """
        pass
