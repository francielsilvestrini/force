#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app()

from kivy.factory import Factory
from kivy.uix.screenmanager import Screen
from kivy.uix.accordion import Accordion
from kivy.uix.accordion import AccordionItem
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from actionbar import CustomActionBar
from widgets import MenuLayout

from screens import Screens


class MenuCustomer(AccordionItem):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Clientes')
        super(MenuCustomer, self).__init__(**kwargs)
        layout = MenuLayout()
        
        btn = Button(text='Novo Cliente')
        btn.bind(on_release=self.do_customer_new)
        layout.add_widget(btn)

        btn = Button(text='Listar Clientes')
        btn.bind(on_release=self.do_customer_list)
        layout.add_widget(btn)

        btn = Button(text='Agenda de Visitas')
        btn.bind(on_release=self.do_calendar)
        layout.add_widget(btn)

        btn = Button(text='Personalizar Filtro de Clientes')
        btn.bind(on_release=self.do_customer_filter)
        layout.add_widget(btn)

        self.add_widget(layout)

    def do_customer_filter(self, instance):
        Screens.create_and_show('CustomerFilter')

    def do_customer_new(self, instance):
        sc = Screens.create('CustomerEditor')
        sc.previous = 'Menu'
        sc.record_key = ''
        sc.reset()
        app.sm.current = 'CustomerEditor'
    
    def do_customer_list(self, instance):
        Screens.create_and_show('CustomerList')

    def do_calendar(self, instance):
        pass


class MenuCatalog(AccordionItem):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Catálogo')
        super(MenuCatalog, self).__init__(**kwargs)
        layout = MenuLayout()
        
        btn = Button(text='Exibir Catálogo')
        btn.bind(on_release=self.do_show_catalog)
        layout.add_widget(btn)

        btn = Button(text='Consultar Preço')
        btn.bind(on_release=self.do_check_price)
        layout.add_widget(btn)

        btn = Button(text='Personalizar Catálogo')
        btn.bind(on_release=self.do_custom_catalog)
        layout.add_widget(btn)

        btn = Button(text='Listar Produtos')
        btn.bind(on_release=self.do_products_list)
        layout.add_widget(btn)

        self.add_widget(layout)

    def do_show_catalog(self, instance):
        pass

    def do_check_price(self, instance):
        pass
    def do_custom_catalog(self, instance):
        pass
    def do_products_list(self, instance):
        sc = Screens.create('ProductsList')
        sc.previous = 'Menu'
        sc.reset()
        app.sm.current = 'ProductsList'


class MenuOrder(AccordionItem):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Pedidos')
        super(MenuOrder, self).__init__(**kwargs)
        layout = MenuLayout()
        
        btn = Button(text='Novo Pedido')
        btn.bind(on_release=self.do_order_new)
        layout.add_widget(btn)

        btn = Button(text='Pedidos em Aberto')
        btn.bind(on_release=self.do_order_open)
        layout.add_widget(btn)

        btn = Button(text='Histórico do cliente')
        btn.bind(on_release=self.do_history)
        layout.add_widget(btn)

        self.add_widget(layout)

    def do_order_new(self, instance):
        pass
    def do_order_open(self, instance):
        pass
    def do_history(self, instance):
        pass


class MenuOthers(AccordionItem):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'Outros')
        super(MenuOthers, self).__init__(**kwargs)
        layout = MenuLayout()
        
        btn = Button(text='Sincronizar')
        btn.bind(on_release=self.do_sync)
        layout.add_widget(btn)

        btn = Button(text='Configuração')
        btn.bind(on_release=self.do_config)
        layout.add_widget(btn)

        self.add_widget(layout)

    def do_sync(self, instance):
        Screens.create_and_show('MenuSync')
        pass

    def do_config(self, instance):
        app.open_settings()


class MenuOptions(Accordion):
    def __init__(self, **kwargs):
        super(MenuOptions, self).__init__(**kwargs)
        self.add_widget(MenuCustomer())
        self.add_widget(MenuCatalog())
        self.add_widget(MenuOrder())
        self.add_widget(MenuOthers())


class Menu(Screen):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(name='Menu', **kwargs)

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(CustomActionBar(title='Onnix Force'))
        layout.add_widget(MenuOptions())
        self.add_widget(layout)
