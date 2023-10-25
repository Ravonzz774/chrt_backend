import requests
from bs4 import BeautifulSoup

def get():
    r = requests.get('https://www.radiotech.su/news/')

    html = r.content

    soup = BeautifulSoup(html, 'html.parser')

    elements = soup.select('body > div.container.text-center > a')

    j = 0

    news = []
    for i in elements:
        j+=1

        body_url = i["href"]

        style = i.find(class_='photo')['style']

        start_index = style.index('url("') + 5
        end_index = style.index('")')
        img_url = style[start_index:end_index]

        img_url = "https://www.radiotech.su" + img_url

        name = i.find(class_ = "h2").text
        date = i.find(class_ = "date").text

        body_block = requests.get("https://www.radiotech.su" + body_url)

        body_parse = BeautifulSoup(body_block.content, 'html.parser')

        body = str(body_parse.select_one("body > div:nth-child(5) > div > div"))


        news.append({
            "title": name,
            "date": date,
            "img": img_url,
            "body": body,
        })
    
    return news

    
