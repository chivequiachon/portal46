from bs4 import BeautifulSoup

import requests


def get_notifications_page(auth_key, username, password):
  login_data = {'auth_key': auth_key, 'ips_username': username, 'ips_password': password}
  
  s = requests.session()
  s.post('https://onehallyu.com/index.php?app=core&module=global&section=login&do=process', login_data)
  r = s.get('https://onehallyu.com/index.php?app=core&module=usercp&tab=core&area=notificationlog')
  
  return r.text


def get_notifications(notifications_page):
  soup = BeautifulSoup(notifications_page, 'html.parser')

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
