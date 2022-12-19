from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import requests
import json

from config import BaseYandexDisk, LOGIN_URL, START_GET_TOKEN_IFRAME_XPATH, START_GET_TOKEN_BUTTON_XPATH,\
                   LOGIN_USER_NAME_LABEL_XPATH, LOGIN_USER_NAME_BUTTON_XPATH, LOGIN_USER_NAME_ERROR_XPATH,\
                   LOGIN_USER_PASSWORD_LABEL_XPATH, LOGIN_USER_PASSWORD_BUTTON_XPATH, LOGIN_USER_PASSWORD_ERROR_XPATH,\
                   USER_TOKEN_IFRAME_XPATH, USER_TOKEN_XPATH
from time import sleep


class YandexDisk(BaseYandexDisk):
    def get_token_start(self):
        self.get(LOGIN_URL)
        self.switch_to.frame(self.find_element(By.XPATH, START_GET_TOKEN_IFRAME_XPATH))
        self.find_element(By.XPATH, START_GET_TOKEN_BUTTON_XPATH).click()
        self.switch_to.default_content()
        sleep(3)

    def get_token_login(self, user_name: str) -> bool:
        self.find_element(By.XPATH, LOGIN_USER_NAME_LABEL_XPATH).send_keys(user_name)
        sleep(3)

        self.find_element(By.XPATH, LOGIN_USER_NAME_BUTTON_XPATH).click()
        sleep(3)

        try:
            self.find_element(By.XPATH, LOGIN_USER_NAME_ERROR_XPATH)

            print("Такого аккаунта не существует")
            return False
        except NoSuchElementException:
            self.user_name = user_name
            sleep(3)
            return True

    def get_token_password(self, user_password: str) -> bool:
        self.find_element(By.XPATH, LOGIN_USER_PASSWORD_LABEL_XPATH).send_keys(user_password)

        self.find_element(By.XPATH, LOGIN_USER_PASSWORD_BUTTON_XPATH).click()
        sleep(3)

        try:
            self.find_element(By.XPATH, LOGIN_USER_PASSWORD_ERROR_XPATH)
            print("Неверный пароль")
            return False
        except NoSuchElementException:
            self.user_password = user_password
            sleep(2)
            return True

    def save_data(self, user_name: str, user_password: str) -> None:
        with open("data.json", "w") as file:
            data = {
                    "user_name": user_name,
                    "user_password": user_password,
                    "user_token": self.disk_token
                   }
            file.write(json.dumps(data))

    def get_token(self) -> bool:
        self.switch_to.frame(self.find_element(By.XPATH, USER_TOKEN_IFRAME_XPATH))
        self.disk_token = self.find_element(By.XPATH, USER_TOKEN_XPATH).get_attribute('value')

        self.save_data(self.user_name, self.user_password)

        return True

    @staticmethod
    def upload_files(token: str, urls: list) -> None:
        requests.put("https://cloud-api.yandex.net/v1/disk/resources",
                     headers={
                         "Authorization": f"OAuth {token}"
                     },
                     params={
                         "path": "/IMG/"
                     })
        for num, url in enumerate(urls):
            requests.post(
                           "https://cloud-api.yandex.net/v1/disk/resources/upload",
                           headers={
                                        "Authorization": f"OAuth {token}"
                                    },
                           params={
                                        "url": url,
                                        "path": f"/IMG/photo_{num + 1}.png",
                                   })

    @staticmethod
    def check_token(token: str) -> bool:
        data_disk = requests.get("https://cloud-api.yandex.net/v1/disk/",
                                 headers={
                                     "Authorization": f"OAuth {token}"
                                 })
        return data_disk.status_code == 200
