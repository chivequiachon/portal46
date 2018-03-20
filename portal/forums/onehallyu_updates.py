from portal.forums.forum_check_strategy import ForumCheckStrategy
from bs4 import BeautifulSoup

import requests


class OneHallyuCheckStrategy(ForumCheckStrategy):
    def __init__(self, username, password, auth_key):
        self.username = username
        self.password = password
        self.auth_key = auth_key

    def request_page(self):
        login_data = {'auth_key': self.auth_key, 'ips_username': self.username, 'ips_password': self.password}

        s = requests.session()
        s.post('https://onehallyu.com/index.php?app=core&module=global&section=login&do=process', login_data)
        r = s.get('https://onehallyu.com/index.php?app=core&module=usercp&tab=core&area=notificationlog')

        return r.text

    def scrape(self, page):
        soup = BeautifulSoup(page, 'html.parser')

        ipb_table = soup.find('table', class_='ipb_table')
        trs = ipb_table.find_all('tr')
        trs.pop(0)

        notifs = []
        for tr in trs:
            notification_html = tr.find('h4')
            date_posted = tr.find('td', class_="col_n_date desc").get_text()

            log = "({}) {}".format(date_posted, notification_html)
            log = log.replace("<h4>", "").replace("</h4>", "")

            notifs.append(log)

        return notifs

