from yandex_disk import check_token, GetApiDisk, upload_files
from config import BASE_DIR
from get_photo_url import get_url_photo

import os
import re
from os.path import isfile
import json

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('2.1.0')


class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)


class registrationApp(Screen):
    def press_check_account_button(self, value):
        disk = GetApiDisk(str(BASE_DIR / "drivers/chromedriver.exe"))
        if disk.get_api(self.user_name.text, self.user_password.text):
            self.process.text = "Вы успешно вошли в свой аккаунт"
            self.manager.transition.direction = 'left'
            self.manager.current = 'upload_files'
        else:
            self.process.text = "Вы неправильно вели логин/пароль"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = TextInput(multiline=False)
        self.user_password = TextInput(multiline=False)

        user_data = GridLayout(rows=3, cols=2, spacing=10,
                               size_hint=(0.7, 0.2))
        user_data.add_widget(Label(text="Введите свой логин"))
        user_data.add_widget(self.user_name)

        user_data.add_widget(Label(text="Введите свой пароль"))
        user_data.add_widget(self.user_password)

        button = Button(text="Войти")
        button.bind(on_press=self.press_check_account_button)
        user_data.add_widget(button)

        self.process = Label(text="")
        user_data.add_widget(self.process)

        page = AnchorLayout(anchor_x="center", anchor_y="center")
        page.add_widget(user_data)

        self.add_widget(page)


class uploadFileApp(Screen):
    def press_get_photo_button(self, value):
        urls = get_url_photo(self.search.text, self.page.text)

        with open("data.json", "r") as file:
            user_data = json.loads(file.read())

        upload_files(user_data["user_token"], urls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data_search = GridLayout(rows=3, cols=2, spacing=20,
                                 size_hint=(0.8, 0.25))

        self.search = TextInput(multiline=False)
        self.page = FloatInput(multiline=False)

        self.page.input_type = "number"

        data_search.add_widget(Label(text="Что хотите получить"))
        data_search.add_widget(self.search)

        data_search.add_widget(Label(text="Какую страницу вы хотите получить"))
        data_search.add_widget(self.page)

        get_photo_button = Button(text="Получить")
        get_photo_button.bind(on_press=self.press_get_photo_button)

        data_search.add_widget(get_photo_button)

        page = AnchorLayout(anchor_x="center", anchor_y="center")
        page.add_widget(data_search)

        self.add_widget(page)


class checkAccount(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        next_button = Button(text="Продолжить")
        exit_account = Button(text="Выйти из аккаунта")

        next_button.bind(on_press=self.press_next_button)
        exit_account.bind(on_press=self.press_exit_account)

        choice = BoxLayout(orientation="vertical", size_hint=(0.6, 0.3), spacing=20)
        choice.add_widget(next_button)
        choice.add_widget(exit_account)

        page = AnchorLayout(anchor_x="center", anchor_y="center")
        page.add_widget(choice)
        self.add_widget(page)

    def press_next_button(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current = 'upload_files'

    def press_exit_account(self, value):
        os.remove("data.json")
        self.manager.transition.direction = 'up'
        self.manager.current = 'registration_account'


class mainApp(App):
    def build(self):
        sm = ScreenManager()
        if isfile("data.json"):
            with open("data.json", "r") as file:
                data = json.loads(file.read())

            if check_token(data["user_token"]):
                sm.add_widget(checkAccount(name="check_account"))
        sm.add_widget(registrationApp(name="registration_account"))

        sm.add_widget(uploadFileApp(name="upload_files"))
        return sm


if __name__ == '__main__':
    mainApp().run()
