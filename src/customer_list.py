#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, DictProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup

from panellistview import PanelListView, PanelListContent, PanelListItem
from customs import CustomActionBar
from customer_form import CustomerFormScreen

from kivy.lang import Builder
Builder.load_string('''
<CustomerItem>
    BoxLayout:
        pos: root.pos
        GridLayout:
            cols: 1
            GridLayout:
                cols: 2

                Label:
                    size_hint_x: .75
                    markup: True
                    text: u'{0}[size=13sp][color=999999]  {1}[/color][/size]'.format(root.data['name'], root.data['full_name'])
                    font_size: '15sp'
                    text_size: self.width-10, None
                Label:
                    size_hint_x: .25
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Ultima Visita', root.data.get('last_visit') or '')
                    font_size: '15sp'
                    text_size: self.width-10, None,

            GridLayout:
                cols: 3

                Label:
                    size_hint_x: .25
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Fone', root.data.get('phone') or '')
                    font_size: '15sp'
                    text_size: self.width-10, None
                Label:
                    size_hint_x: .5
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Cidade', root.data.get('address_city') or '')
                    font_size: '15sp'
                    text_size: self.width-10, None
                Label:
                    size_hint_x: .25
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Proxima Visita', root.data.get('next_visit') or '')
                    font_size: '15sp'
                    text_size: self.width-10, None


''');


class CustomerListActionBar(CustomActionBar):
    def do_previous(self):
        s = self.parent.parent
        s.back_filter()
        return True

class CustomerItem(PanelListItem):
    key = StringProperty()
    data = DictProperty(None)

class SettingSpacer(Widget):
    # Internal class, not documented.
    pass

class CustomerListScreen(Screen):
    popup = ObjectProperty(None, allownone=True)
    textinput = ObjectProperty(None)
    value = StringProperty(None)

    def __init__(self, name, **kwargs):
        super(CustomerListScreen, self).__init__(name=name, **kwargs)
        self.back_filter()

    def do_release(self, instance):
        sm = self.manager
        sc = CustomerFormScreen(name='customer_edit', key=instance.key)
        sm.add_widget(sc)
        sm.current = 'customer_edit'

    def do_show_all(self, instance):
        self.update_list()
        return

    def do_show_by_city(self, instance):
        for k in globals():
            print k
        return
        
    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value
        self.update_list()

    def do_show_by_identify(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title='Identificação', content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))

        # create the textinput used for numeric input
        self.textinput = textinput = TextInput(
            text='', font_size='24sp', multiline=False,
            size_hint_y=None, height='42sp')
        textinput.bind(on_text_validate=self._validate)
        self.textinput = textinput

        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()
        return

    def back_filter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')

        actionbar = CustomActionBar(title='Listar Clientes')
        layout.add_widget(actionbar)

        buttons = GridLayout(cols=1, row_default_height='40dp', row_force_default=True)
        buttons.add_widget(Button(text='Exibir Todos', on_press=self.do_show_all))
        buttons.add_widget(Button(text='Filtrar por Cidade', on_press=self.do_show_by_city))
        buttons.add_widget(Button(text='Filtrar por Identificação', on_press=self.do_show_by_identify))

        layout.add_widget(buttons)
        self.add_widget(layout)
        return

    def update_list(self):
        store = JsonStore('data/customers.json')

        content = PanelListContent()
        for key in store:
            record = store[key]

            item = None
            if self.value:
                if self.value in record['name']:
                    item = CustomerItem(key=key, data=store[key])
            else:
                item = CustomerItem(key=key, data=store[key])

            if item:
                item.bind(on_release=self.do_release)
                content.add_widget( item )

        view = PanelListView()
        view.add_widget(content)

        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')

        actionbar = CustomerListActionBar(title='Todos os Clientes')
        layout.add_widget(actionbar)
        layout.add_widget(view)

        self.add_widget(layout)
        return

