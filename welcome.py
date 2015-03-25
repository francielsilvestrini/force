#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class Welcome(Screen):

    def __init__(self, **kwargs):
        super(Welcome, self).__init__(name='Welcome', **kwargs)

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Image(source='images/logo.png'))
        layout.add_widget(Label(text='Bem Vindo ao Onnix Force', font_size=36))
        layout.add_widget(Label(text='ONNIX SISTEMAS'))

        self.add_widget(layout)
