#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0'

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithSidebar

from settings_json import settings_json
from data_json import DataJson

Window.softinput_mode = 'pan'
Window.keyboard_height = 100

Factory.register('Welcome', module='welcome')
Factory.register('Login', module='login')
Factory.register('Menu', module='menu')
Factory.register('CustomerFilter', module='customer_filter')
Factory.register('CitiesList', module='cities_list')
Factory.register('MenuSync', module='sync')
Factory.register('Sync', module='sync')
Factory.register('CustomerList', module='customer_list')
Factory.register('CustomerEditor', module='customer_editor')
Factory.register('ProductsList', module='products_list')


class OnnixForceApp(App):
    sm = ScreenManager()

    def __init__(self, **kwargs):
        super(OnnixForceApp, self).__init__(**kwargs)

        self.config_changed = False
        self.DB = DataJson()

        self.sm.add_widget(Factory.Welcome())
        self.sm.add_widget(Factory.Login())
        self.sm.add_widget(Factory.Menu())

        #self.sm.add_widget(Factory.CustomerEditor())

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = True
        self.icon = 'images/icon.png'

        return self.sm

    def on_start(self):
        self.DB.start()
        username = self.config.get('onnixforce', 'username')
        if username == '':
            self.open_settings()
        else:
            self.sm.current = 'Login'
            #self.sm.current = 'CustomerEditor'

    def build_config(self, config):
        config.setdefaults('onnixforce', {
            'username':'',
            'password':'',  
            'api_hostname':'http://www.onnixsistemas.com.br',
            'api_endpoint':'/onnixforce/api',
            'states':'PR SC RS',
            'customer_update_server': 'all',
            'product_update_server': 'all',
            })

    def build_settings(self, settings):
        settings.add_json_panel('Onnix Force', self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        self.config_changed = True

    def close_settings(self, *args):
        if self.config.get('onnixforce', 'username') == '':
            self.stop()
        else:
            super(OnnixForceApp, self).close_settings(*args)
            if self.config_changed:
                self.sm.current = 'Login'
            return True

if __name__ == '__main__':
    OnnixForceApp().run()