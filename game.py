from bs4 import BeautifulSoup as BS
import requests


# получение топ 10 самых лучших игр
def game():
    url = requests.get('https://www.geeksforgeeks.org/most-played-online-games-2024/')
    html = BS(url.content, 'html.parser')
    a = []
    for el in html.select(".text"):
        z = el.select(".wp-caption > img")
        for j in z:
            a.append((j['alt'], j['src']))
    return a
