from config import BASE_DIR
from yandex_disk import GetApiDisk, upload_files
from get_photo_url import get_url_photo

if __name__ == "__main__":
    disk = GetApiDisk(str(BASE_DIR / "drivers/chromedriver.exe"))

    api = None

    user_name = input("Введите ваш логин или email: ")
    user_password = input("Введите ваш пароль: ")

    if disk.get_api(user_name, user_password):
        api = disk.disk_api

    upload_files(api, get_url_photo("break", 2))
