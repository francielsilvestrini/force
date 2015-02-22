#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0'

import kivy
kivy.require('1.8.0')

from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore

from settings_json import settings_json
from menu import MenuScreen
from customs import CustomTextInput
from customs import AppSettings

Builder.load_file('onnixforce.kv')
Window.softinput_mode = 'pan'
Window.keyboard_height = 100

app = App.get_running_app
sm = ScreenManager()

class StartScreen(Screen):
    pass


class LoginScreen(Screen):
    username_box = ObjectProperty()
    password_box = ObjectProperty()

    def on_login(self):
        usr = app().config.get('onnixforce', 'username')
        pwd = app().config.get('onnixforce', 'password')
        if (usr == self.username_box.text) and (pwd == self.password_box.text):
            sm.current = 'menu'
        else:
            btnclose = Button(text='Fechar', size_hint_y=None, height='50sp')
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='Usuário ou Senha inválido!'))
            content.add_widget(btnclose)
            popup = Popup(content=content, title='Atenção',
                      size_hint=(None, None), size=('300dp', '300dp'))
            btnclose.bind(on_release=popup.dismiss)
            popup.open()

    def on_close(self):
        app().stop()
    

sm.add_widget(StartScreen(name='start'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(MenuScreen(name='menu'))

class OnnixForceApp(App):
    
    def __init__(self, **kwargs):
        super(OnnixForceApp, self).__init__(**kwargs)
        self.config_changed = False

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = True
        return sm

    def build_config(self, config):
        config.setdefaults('onnixforce', {
            'username':'',
            'password':'',  
            'api_hostname':'http://www.onnixforce.com.br',
            'api_hostport': 80,
            'api_endpoint':'/api/ws',
            'states':'PR SC RS',
            'customer_update_server': datetime.today().strftime(AppSettings.datetime_format),
            })

    def build_settings(self, settings):
        settings.add_json_panel('Onnix Force', self.config, data=settings_json)

    def on_start(self):
        username = self.config.get('onnixforce', 'username')
        if username == '':
            self.open_settings()
        else:
            sm.current = 'login'

    def on_config_change(self, config, section, key, value):
        self.config_changed = True

    def close_settings(self, *args):
        if self.config.get('onnixforce', 'username') == '':
            self.stop()
        else:
            super(OnnixForceApp, self).close_settings(*args)
            if self.config_changed:
                sm.current = 'login'
            return True

if __name__ == '__main__':
    OnnixForceApp().run()