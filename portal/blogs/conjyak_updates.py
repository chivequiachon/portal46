from portal.blogs.blog_check_strategy import BlogCheckStrategy
from bs4 import BeautifulSoup

import requests


class ConjyakCheckStrategy(BlogCheckStrategy):
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def request_page(self):
        r = requests.get("https://conjyak.wordpress.com/{}/{}/".format(self.year, self.month))
        return r.text

    def scrape(self, page):
        soup = BeautifulSoup(page, 'html.parser')

        articles = soup.find_all('article')

        updates = []
        for article in articles:
            h2 = article.find('header').find('h2')
            href = h2.find('a').get('href')
            title = h2.text
            
            date_temp = href.split("/")
            date = "{}-{}-{}".format(date_temp[3], date_temp[4], date_temp[5])

            updates.append("<strong>[{}]</strong> <a href=\"{}\">{}</a>".format(date, href, title))

        return updates

