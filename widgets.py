#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty


class FormLayout(GridLayout):
    '''
    Layout com 2 columas e altura padrão de 40dp
    '''
    def __init__(self, **kwargs):
        kwargs.setdefault('cols', 2)
        kwargs.setdefault('spacing', 10)
        kwargs.setdefault('padding', 10)
        kwargs.setdefault('row_default_height', '40dp')
        kwargs.setdefault('row_force_default', True)
        super(FormLayout, self).__init__(**kwargs)

class MenuLayout(GridLayout):
    '''
    Layout com 1 columas e altura padrão de 40dp
    '''
    def __init__(self, **kwargs):
        kwargs.setdefault('cols', 1)
        kwargs.setdefault('spacing', 10)
        kwargs.setdefault('padding', 20)
        kwargs.setdefault('row_default_height', '40dp')
        kwargs.setdefault('row_force_default', True)
        super(MenuLayout, self).__init__(**kwargs)


class HCFScreen(Screen):
    '''
    Desenho padrão de uma janela com cabeçalho, conteudo e rodapé,
    geralmente usada para formularios
    '''

    previous = StringProperty('Menu')

    def __init__(self, name, **kwargs):
        super(HCFScreen, self).__init__(name=name, **kwargs)

        layout = BoxLayout(orientation='vertical')
        self.header = BoxLayout(**{'size_hint':(1,None), 'size':(1,40)})
        self.content = BoxLayout()
        self.footer = BoxLayout(**{'size_hint':(1,None), 'size':(1,40)})
        layout.add_widget(self.header)
        layout.add_widget(self.content)
        layout.add_widget(self.footer)
        self.add_widget(layout)

    def reset(self):
        pass


class SearchLayout(GridLayout):

    def __init__(self, **kwargs):
        kwargs.setdefault('cols', 4)
        kwargs.setdefault('spacing', 4)
        kwargs.setdefault('padding', 0)
        kwargs.setdefault('row_default_height', '40dp')
        kwargs.setdefault('row_force_default', True)
        kwargs.setdefault('size_hint', (1,None) )
        kwargs.setdefault('size', (1,40))
        super(SearchLayout, self).__init__(**kwargs)
