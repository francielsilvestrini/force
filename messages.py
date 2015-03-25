#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.widget import Widget

class MessageBox(object):
    
    def __init__(self, text, title='Atenção', auto_open=True, size=('300dp', '300dp'), **kwargs):
        super(MessageBox, self).__init__(**kwargs)
        btnclose = Button(text='Fechar', size_hint_y=None, height='50sp')

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=text))
        content.add_widget(btnclose)
        self.popup = Popup(content=content, title=title,
                  size_hint=(None, None), size=size)
        btnclose.bind(on_release=self.popup.dismiss)
        if auto_open:
            self.open()

    def open(self):
        self.popup.open()        

class MessageBoxContent(object):
    
    def __init__(self, content, title='Atenção', auto_open=True, size=('300dp', '300dp'), **kwargs):
        super(MessageBoxContent, self).__init__(**kwargs)
        btnclose = Button(text='Fechar', size_hint_y=None, height='50sp')

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(content)
        layout.add_widget(btnclose)
        self.popup = Popup(content=layout, title=title,
                  size_hint=(None, None), size=size)
        btnclose.bind(on_release=self.popup.dismiss)
        if auto_open:
            self.open()

    def open(self):
        self.popup.open()   