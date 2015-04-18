from bs4 import BeautifulSoup

__all__ = ('Parser')


class Parser:
    def __init__(self, html):
        self.bs = BeautifulSoup(html)

    @property
    def lang(self):
        return self.bs.find('html').get('lang')

    @property
    def can_allow_parse(self):
        return True

    def run(self):
        if not self.can_allow_parse:
            return {}
        return self.serialize()

    def serialize(self):
        return {}
