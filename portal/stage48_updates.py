from bs4 import BeautifulSoup

import requests


def get_alerts_page(username, password):
  login_data = {'login': username, 'password': password}
  
  s = requests.session()
  r = s.post("http://www.stage48.net/forum/index.php?login/login", login_data)
  r2 = s.get("http://www.stage48.net/forum/index.php?account/alerts")
  return r2.text
  
  
def get_alerts(alerts_page):
  soup = BeautifulSoup(alerts_page, "html.parser")

  alert_group = soup.find('li', class_="alertGroup")
  day = alert_group.find('h2').get_text()

  alerts = []
  for li in alert_group.find_all('li'):
    poster = li.get('data-author')
    time = li.find('div', class_="timeRow").get_text()
    thread = li.find('a', class_="PopupItemLink")
    thread_name = thread.get_text()
    poster_link = "http://www.stage48.net/forum/" + li.find('a').get('href')
    thread_link = "http://www.stage48.net/forum/" + thread.get('href')
    
    h3 = li.find('h3')
    text = h3.get_text()
    
    text = text.replace(poster, "<a href=\"{}\"><strong>{}</strong></a>".format(poster_link, poster))
    text = text.replace(thread_name, "<a href=\"{}\"><strong>{}</strong></a>".format(thread_link, thread_name))
    
    text = "[{}][{}]{}".format(day, time, text)
    alerts.append(text)
    
  return alerts
