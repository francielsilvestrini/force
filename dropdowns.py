#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
app = App.get_running_app()

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

class StatesDropDown(DropDown):
    '''
    Prove a lista de Estados configurados no dispositivo, 
    para exibição no formado de dropdown
    '''
    _owner = ObjectProperty()

    def load(self, owner):
        self._owner = owner
        self.clear_widgets()
        states = app.config.get('onnixforce', 'states').split(' ')
        states = ['<Limpar>'] + states
        for state in states:
            btn = Button(text=state, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select(btn.text))
            self.add_widget(btn)
        
        #self.bind(on_select=lambda instance, x: setattr(owner, 'text', x))
        self.bind(on_select=self.do_select)

    def do_select(self, instance, value):
        self._owner.text = app.DB.select_text if value == '<Limpar>' else value
        self._owner.update_select()


states_dropdown = StatesDropDown()
