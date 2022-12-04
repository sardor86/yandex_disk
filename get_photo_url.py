import requests
from bs4 import BeautifulSoup

from config import GET_PHOTO_URL_FREEPIK, BROWSER_SETTINGS


def get_url_photo(query: str, page: int) -> list:
    content = requests.get(GET_PHOTO_URL_FREEPIK,
                           headers={'User-Agent': BROWSER_SETTINGS},
                           params={"format": "search",
                                   "page": page,
                                   "query": query})

    page = BeautifulSoup(content.content, "html.parser")
    img_figures = page.find("div", class_="list-content").find("section").find("div").find_all("figure")
    url = []
    for img_figure in img_figures:
        try:
            url_img = img_figure.find("div").find("a").find("img").get("src")[0:-18]
            if url_img[-1] == "g":
                url.append(url_img)
        except AttributeError:
            continue
    return url
