#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager

from customs import CustomActionBar

from kivy.lang import Builder
Builder.load_string('''
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        CustomActionBar:
            title: 'Onnix Force'

        Accordion:
            AccordionItem:
                title: 'Clientes'
                GridLayout:
                    cols: 1
                    row_default_height: '40dp'
                    row_force_default: True
                    Button:
                        text: 'Agenda de Visitas'
                        on_press: root.goto('calendar')
                    Button:
                        text: 'Selecionar Cliente'
                        on_press: root.goto('select_customer')
                    Button:
                        text: 'Novo Cliente'
                        on_press: root.goto('customer_form')
                    Button:
                        text: 'Listar Clientes'
                        on_press: root.goto('customer_list')
            AccordionItem:
                title: 'Catálogo'
                GridLayout:
                    cols: 1
                    row_default_height: '40dp'
                    row_force_default: True
                    Button:
                        text: 'Exibir Catálogo'
                    Button:
                        text: 'Consultar Preço'
                    Button:
                        text: 'Exibir'
            AccordionItem:
                title: 'Pedidos'
                GridLayout:
                    cols: 1
                    row_default_height: '40dp'
                    row_force_default: True
                    Button:
                        text: 'Novo Pedido'
                    Button:
                        text: 'Pedidos Recentes'
            AccordionItem:
                title: 'Outros'
                GridLayout:
                    cols: 1
                    row_default_height: '40dp'
                    row_force_default: True
                    Button:
                        text: 'Sincronizar'
                        on_press: root.goto('sync_menu')
                    Button:
                        text: 'Selecionar Região'
                        on_press: root.goto('select_state')
                    Button:
                        text: 'Configuração'
                        on_press: root.goto('config')
''')

from customer_form import CustomerFormScreen
from customer_list import CustomerListScreen
from calendar import CalendarScreen
from sync import SyncMenuScreen

screen_map = dict(
    customer_form=CustomerFormScreen,
    customer_list=CustomerListScreen,
    calendar=CalendarScreen,
    sync_menu=SyncMenuScreen,
    )

class MenuScreen(Screen):
    def create_screen(self, new_screen):
        sm = self.manager
        if not sm.has_screen(new_screen):
            cls = screen_map.get(new_screen)
            sc = cls(name=new_screen)
            sm.add_widget(sc)
        else:
            sc = sm.get_screen(new_screen)
        return sc

    def goto(self, new_screen):
        if new_screen == 'config':
            app = App.get_running_app()
            app.open_settings()
        else:
            sm = self.manager
            self.create_screen(new_screen)
            sm.current = new_screen


    def on_close(self):
        app = App.get_running_app()
        app.stop()