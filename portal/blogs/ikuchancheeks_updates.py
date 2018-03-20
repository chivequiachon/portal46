from portal.blogs.blog_check_strategy import BlogCheckStrategy
from bs4 import BeautifulSoup

import requests


class IkuchancheeksCheckStrategy(BlogCheckStrategy):
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def request_page(self):
        r = requests.get("https://ikuchancheeks.blogspot.co.id/{}/{:02d}".format(self.year, self.month))
        return r.text

    def scrape(self, page):
        soup = BeautifulSoup(page, 'html.parser')

        blog_post_containers = soup.find_all('div', class_='date-outer')

        updates = []
        for container in blog_post_containers:
            blog_posts = container.find_all('div', class_="post-outer")

            for post in blog_posts:
                h2 = post.find('h2', class_="post-title entry-title")
                title = h2.text.strip(' \t\n\r')
                date = post.find('span', class_='bpostdate').text.strip(' \t\n\r')
                href = h2.find('a').get('href')
                updates.append("<strong>[{}]</strong> <a href=\"{}\">{}</a>".format(date, href, title))

        return updates

