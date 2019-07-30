import bs4
import requests as rqs

from web_scrapper.common import config


class NewsPage:
    def __init__(self, news_site_uid,url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)

    def _select(self, query):
        return self._html.select(query)

    def _visit(self, url):
        response = rqs.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class Homepage(NewsPage):
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def article_links(self):
        link_list = []
        ls = self._select(self._queries['homepage_article_links'])
        for link in ls:
            if link and link.has_attr('href'):
                link_list.append(link)

        return link_list


class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''
