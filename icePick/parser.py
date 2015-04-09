from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
        self.bs = BeautifulSoup(html.decode('utf-8', 'ignore'))

    @property
    def can_allow_parse(self):
        return True

    def run(self):
        result = {}
        if not self.can_allow_parse:
            return result
        return result
