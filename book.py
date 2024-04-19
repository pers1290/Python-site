from bs4 import BeautifulSoup as BS
import requests


# получение топ 10 самых лучших книг
def book():
    url = requests.get('https://www.livelib.ru/selection/2666008-10-samyh-populyarnyh-knig-v-knizhnom-vyzove-2023')
    html = BS(url.content, 'html.parser')

    a = []
    for el in html.select(".cover-wrapper"):
        z = el.select("a > img")
        a.append((z[0]['alt'], z[0]['data-pagespeed-lazy-src']))
    return a
