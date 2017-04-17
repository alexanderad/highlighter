import bs4


class VacuumCleaner(object):
    EXTRACT_FILTERS = (
        ('div', {'class': 'article-share'}),
    )

    def __init__(self, html):
        self._soup = bs4.BeautifulSoup(html, 'lxml')

    def clean(self):
        for selector in self.EXTRACT_FILTERS:
            for item in self._soup.find_all(*selector):
                item.extract()

    def __repr__(self):
        return self._soup.prettify('utf-8', formatter='html')

    def apply_all(self):
        self.clean()
        return repr(self)
