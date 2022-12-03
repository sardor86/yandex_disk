import requests
from bs4 import BeautifulSoup
from .config import GET_PHOTO_URL_FREEPIK


def get_url_photo(query: str, page: int) -> list:
    content = requests.get(GET_PHOTO_URL_FREEPIK,
                           headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 '
                                                  'Safari/537.36'},
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
