import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    tablichka = parser.table.findAll("table")[1]
    nov = tablichka.findAll("tr")
    slovar_nov = {"title": "None", "url": "None", "author": "None", "points": 0}
    for i in range(len(nov)):
        stroka = nov[i]
        if i % 3 == 0:
            slovar_nov = {
                "title": "None",
                "url": "None",
                "author": "None",
                "points": 0,
                "comments": 0,
            }
        elif i % 30 == 0:
            slovar_nov = {}
        if stroka.attrs:
            if stroka.attrs["class"][0] == "athing":
                slovar_nov["title"] = stroka.find("a", class_="titlelink").string
                ssylka = stroka.find("a", class_="titlelink").get("href")
                if "http" in ssylka:
                    slovar_nov["url"] = ssylka
                elif "item" in ssylka:
                    slovar_nov["url"] = "https://news.ycombinator.com/" + ssylka
        else:
            if stroka.find("a").attrs:
                if (
                    "class" in stroka.find("a").attrs
                    and stroka.find("a").attrs["class"][0] == "hnuser"
                ):
                    slovar_nov["author"] = stroka.find("a").string
                    slovar_nov["points"] = int(stroka.find("span").string.split()[0])
                    com = str(stroka.findAll("a")[-1].string.split()[0])
                    if com.isdigit():
                        slovar_nov["comments"] = int(com)
                    else:
                        slovar_nov["comments"] = 0
            else:
                break
            news_list.append(slovar_nov)
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    return parser.table.findAll("table")[1].findAll("tr")[-1].contents[2].find("a").get("href")


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    nov = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        nov.extend(news_list)
        n_pages -= 1
    return nov
