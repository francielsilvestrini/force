#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from widgets import FormLayout
from customs import CustomTextInput
from messages import MessageBox

class LoginForm(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginForm, self).__init__(**kwargs)

        layout = FormLayout()

        self.username = CustomTextInput()
        self.password = CustomTextInput(password=True)

        layout.add_widget(Label(text='Usuário'))
        layout.add_widget(self.username)

        layout.add_widget(Label(text='Senha'))
        layout.add_widget(self.password)

        btn_login = Button(text='Login')
        btn_login.bind(on_release=self.do_login)

        btn_close = Button(text='Fechar')
        btn_close.bind(on_release=self.do_close)

        buttons = BoxLayout()
        buttons.add_widget(btn_login)
        buttons.add_widget(btn_close)

        layout.add_widget(Widget())
        layout.add_widget(buttons)

        self.add_widget(layout)

    def do_close(self, instance):
        app().stop()

    def do_login(self, instance):
        usr = app().config.get('onnixforce', 'username')
        pwd = app().config.get('onnixforce', 'password')
        if (usr == self.username.text) and (pwd == self.password.text):
            app().sm.current = 'Menu'
        else:
            MessageBox(text='Usuário ou Senha inválido!')


class Login(Screen):

    def __init__(self, **kwargs):
        super(Login, self).__init__(name='Login', **kwargs)

        layout = BoxLayout(orientation='vertical')

        layout_top = BoxLayout(orientation='horizontal')
        layout_top.add_widget(Image(source='images/logo.png'))
        layout_top.add_widget(LoginForm())

        layout_bottom = BoxLayout(orientation='vertical')
        layout_bottom.add_widget(Label(text='Bem Vindo ao Onnix Force', font_size=36))
        layout_bottom.add_widget(Label(text='ONNIX SISTEMAS'))

        layout.add_widget(layout_top)
        layout.add_widget(layout_bottom)
        self.add_widget(layout)
