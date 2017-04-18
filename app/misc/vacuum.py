import bs4

from . import hashies


class Vacuum(object):
    EXTRACT_CSS_SELECTORS = (
        'div.article-share',
    )

    def __init__(self, html, salt=None, https_proxy=None):
        self._soup = bs4.BeautifulSoup(html, 'lxml')
        self._salt = salt
        self._https_proxy = https_proxy

    def clean(self):
        for selector in self.EXTRACT_CSS_SELECTORS:
            map(lambda item: item.extract(), self._soup.select(selector))

    def httpsify(self):
        for img in self._soup.find_all('img'):
            src = img.attrs['src']
            if not src.startswith('https://'):
                signature = hashies.sign_string(src, self._salt)
                img.attrs['src'] = '{}?u={}&s={}'.format(
                    self._https_proxy, src, signature)

    def __repr__(self):
        return self._soup.prettify('utf-8', formatter='substitute_html')

    def apply_all(self):
        self.clean()
        self.httpsify()
        return repr(self)
