class Order:
    def __init__(self, url, ua, method='GET'):
        self.url = url
        self.ua = ua
        self.method = method

    @property
    def user_agent(self):
        return self.ua

    def to_dict(self, html):
        """
        parser = Parser()
        return parser.run()
        """
        return {}

    def save(self, result):
        """
        hoge = Record.create()
        hoge.save(result)
        """
        pass
