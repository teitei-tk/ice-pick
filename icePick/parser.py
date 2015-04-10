from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
        self.bs = BeautifulSoup(html)

    @property
    def can_allow_parse(self):
        return True

    def run(self):
        if not self.can_allow_parse:
            return {}
        return self.serialize()

    def serialize(self):
        pass
