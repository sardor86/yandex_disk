from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pathlib import Path

LOGIN_URL = "https://yandex.ru/dev/disk/poligon/"
BROWSER_SETTINGS = "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"

GET_PHOTO_URL_FREEPIK = "https://www.freepik.com/search"

BASE_DIR = Path(__file__).resolve().parent


class BaseYandexDisk(webdriver.Chrome):
    def __init__(self, driver_path: str):
        options = Options()
        options.add_argument('headless')
        options.add_argument(
            BROWSER_SETTINGS)

        super().__init__(executable_path=driver_path, chrome_options=options)
        print('Браузер готов')

        self.user_name = None
        self.user_password = None
        self.disk_token = None

    def __del__(self):
        self.close()
        self.quit()
        print("Браузер закрыт")


START_GET_TOKEN_IFRAME_XPATH = "/html/body/div[3]/div/div/span/section/div[1]/div[1]" \
                        "/div/section/div/div/section/div/div/div/div[1]/div" \
                        "/section/div/div/div/div[4]/section/div/div/iframe"
START_GET_TOKEN_BUTTON_XPATH = "/html/body/div/section/div[1]/div/a"


LOGIN_USER_NAME_LABEL_XPATH = "/html/body/div/div/div[2]/div[2]/div/div/div[2]"\
                              "/div[3]/div/div/div/div[1]/form/div[2]/div/div[2]"\
                              "/span/input"
LOGIN_USER_NAME_BUTTON_XPATH = "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"\
                               "/div/div/div/div[1]/form/div[4]/button"
LOGIN_USER_NAME_ERROR_XPATH = "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"\
                              "/div/div/div/div[1]/form/div[2]/div/div[2]/div"

LOGIN_USER_PASSWORD_LABEL_XPATH = "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"\
                                  "/div/div/div/form/div[2]/div[1]/span/input"
LOGIN_USER_PASSWORD_BUTTON_XPATH = "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"\
                                   "/div/div/div/form/div[3]/button"
LOGIN_USER_PASSWORD_ERROR_XPATH = "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"\
                                  "/div/div/div/form/div[2]/div[1]/div"

USER_TOKEN_IFRAME_XPATH = "/html/body/div[3]/div/div/span/section/div[1]/div[1]"\
                          "/div/section/div/div/section/div/div/div/div[1]/div/"\
                          "section/div/div/div/div[4]/section/div/div/iframe"
USER_TOKEN_XPATH = "/html/body/div/section/div[1]/span/input"
