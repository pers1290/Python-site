from bs4 import BeautifulSoup as BS
import requests


# получение топ 10 самых лучших фильмов
def parser():
    url = requests.get('https://www.imdb.com/list/ls058596985/')
    html = BS(url.content, 'html.parser')
    a = []
    for el in html.select(".lister-item"):
        z = el.select(".lister-item-image > a > img")
        a.append((z[0]['alt'], z[0]['loadlate']))
    return a
