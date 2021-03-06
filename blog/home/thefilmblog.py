import requests
from bs4 import BeautifulSoup

URL = ["https://thefilm.blog/","https://thefilm.blog/category/news/","https://thefilm.blog/category/previews/","https://thefilm.blog/category/reviews/"]

def get_article(url):
    url_ = url
    article = []
    for p in range(1,3):
        url = url_ + "page/"+str(p)+"/"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        for id, articles in enumerate(soup.find_all("article")):
            category = articles.find("span", {"class": "cat-links"}).get_text()
            title = articles.find("h1").get_text()
            img = articles.find("img").get("data-orig-file")
            detail_url = articles.find("h1").find("a").get("href")
            article.append({"category": category, "title": title, "avatar": img, "url": detail_url})
    return article

def get_detail(detail_url):
    html = requests.get(detail_url).text
    soup = BeautifulSoup(html,"html.parser")
    detail = []
    article = soup.find("article")
    category = article.find("span",{"class": "cat-links"}).get_text()
    title = article.find("h1").get_text()
    created = article.find("span",{"class": "entry-date"}).find("time").get("datetime")
    author = article.find("span", {"class": "author vcard"}).find("a").get_text()
    content = article.find("div", {"class": "entry-content"})
    detail.append({"category":category,"title": title,"created":created,"author":author,"content":content})
    return detail

