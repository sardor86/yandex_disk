from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import requests
import json

from config import LOGIN_URL
import time


class GetApiDisk(webdriver.Chrome):
    def __init__(self, driver_path: str):
        super().__init__(executable_path=driver_path)
        print('Браузер готов')

        self.user_name = None
        self.user_password = None
        self.disk_api = None

    def get_api(self, user_name: str, user_password: str) -> bool:
        ##########################################################################################################
        # login
        self.get(LOGIN_URL)
        time.sleep(2)
        self.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]"
                                    "/div[3]/div/div/div/div[1]/form/div[2]/div/div[2]"
                                    "/span/input").send_keys(user_name)
        time.sleep(3)

        self.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"
                                    "/div/div/div/div[1]/form/div[4]/button").click()
        time.sleep(3)

        try:
            error = self.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"
                                                "/div/div/div/div[1]/form/div[2]/div/div[2]/div")

            print("Такого аккаунта не существует")
            return False
        except NoSuchElementException:
            time.sleep(3)

        ##################################################################################################
        # password

        self.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"
                                    "/div/div/div/form/div[2]/div[1]/span/input").send_keys(user_password)

        self.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"
                                    "/div/div/div/form/div[3]/button").click()
        time.sleep(3)

        try:
            error = self.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]"
                                                "/div/div/div/form/div[2]/div[1]/div")
            print("Неверный пароль")
            return False
        except NoSuchElementException:
            time.sleep(2)

        self.switch_to.frame(self.find_element(By.XPATH, "/html/body/div[3]/div/div/span/section/div[1]/div[1]"
                                                         "/div/section/div/div/section/div/div/div/div[1]/div/"
                                                         "section/div/div/div/div[4]/section/div/div/iframe"))

        self.disk_api = self.find_element(By.XPATH, "/html/body/div/section/div[1]/span/input").get_attribute('value')

        with open("data.json", "w") as file:
            data = {
                    "user_name": user_name,
                    "user_password": user_password,
                    "user_token": self.disk_api
                   }
            file.write(json.dumps(data))

        return True

    def __del__(self):
        self.close()
        self.quit()
        print("Браузер закрыт")


def upload_files(token: str, urls: list) -> None:
    requests.put("https://cloud-api.yandex.net/v1/disk/resources",
                 headers={
                     "Authorization": f"OAuth {token}"
                 },
                 params={
                     "path": "/IMG/"
                 })
    for num, url in enumerate(urls):
        data_upload = requests.post("https://cloud-api.yandex.net/v1/disk/resources/upload",
                                    headers={
                                        "Authorization": f"OAuth {token}"
                                    },
                                    params={
                                        "url": url,
                                        "path": f"/IMG/photo_{num + 1}.png",
                                        "overwrite": True
                                    })