import bs4


class Vacuum(object):
    EXTRACT_CSS_SELECTORS = (
        'div.article-share',
        'div.ad-container',
        'iframe',
    )

    def __init__(self, html):
        self._soup = bs4.BeautifulSoup(html, 'lxml')

    def clean(self):
        for selector in self.EXTRACT_CSS_SELECTORS:
            map(lambda item: item.extract(), self._soup.select(selector))

    def __repr__(self):
        return self._soup.prettify('utf-8')

    def apply_all(self):
        self.clean()
        return repr(self)
