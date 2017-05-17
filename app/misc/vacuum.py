import bs4
import bleach


class Vacuum(object):
    EXTRACT_CSS_SELECTORS = (
        'div.article-share',
        'div.ad-container',
        'iframe',

        'p.content-meta',
        'a.btn.is-fb',
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


class VacuumFull(object):
    def __init__(self, html):
        self._html = html

    def clean(self):
        self._html = bleach.clean(self._html, tags=[], strip=True)

    def strip_newlines(self):
        lines = filter(None, map(unicode.strip, self._html.split('\n')))
        self._html = ' '.join(lines)

    def apply_all(self):
        self.clean()
        self.strip_newlines()
        return self._html
