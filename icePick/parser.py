from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html):
        self.bs = BeautifulSoup(html.decode('utf-8', 'ignore'))

    def run(self):
        return {}
