#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app()

from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import ObjectProperty

from actionbar import CustomActionBar
from widgets import FormLayout
from widgets import HCFScreen

from dropdowns import states_dropdown
from screens import Screens
from messages import MessageBox




class StateSelect(Button):

    __events__ = ('on_update', )

    def __init__(self, **kwargs):
        super(StateSelect, self).__init__(**kwargs)
        preferences = app.DB.preferences

        self.text = preferences.get('customer_filter')['state']
        self.size_hint = (None, None)
        self.bind(on_release=states_dropdown.open)      
        states_dropdown.load(self)

    def update_select(self):
        self.dispatch('on_update')

    def on_update(self):
        pass

#class FilterForm(ScrollView):
class FilterForm(BoxLayout):
    def __init__(self, **kwargs):
        super(FilterForm, self).__init__(**kwargs)

        layout = FormLayout()

        self.state = StateSelect()
        self.state.bind(on_update=self.do_update_select)

        preferences = app.DB.preferences
        self.city = Button(text=preferences.get('customer_filter')['city'])
        self.city.bind(on_release=self.select_city)

        layout.add_widget(Label(text='Estado'))
        layout.add_widget(self.state)

        layout.add_widget(Label(text='Município'))
        layout.add_widget(self.city)

        self.add_widget(layout)

    def do_update_select(self, instance):
        self.city.text = app.DB.select_text

    def select_city(self, instance):
        if self.state.text == app.DB.select_text:
            MessageBox(text='Selecione um estado!')
            return
        sc = Screens.create('CitiesList')
        sc.previous = 'CustomerFilter'
        if sc.state != self.state.text:
            sc.state = self.state.text
            sc.reset()
        sc.bind(on_selected=self.do_selected)
        app.sm.current = 'CitiesList'

    def do_selected(self, instance):
        self.city.text = instance.item_selected.name
        app.sm.current = 'CustomerFilter'

    def save(self):
        row = app.DB.preferences.get('customer_filter')
        row['state'] = self.state.text
        row['city'] = self.city.text
        app.DB.preferences.put('customer_filter', **row)
        return True


class CustomerFilter(HCFScreen):

    def __init__(self, **kwargs):
        super(CustomerFilter, self).__init__(name='CustomerFilter', **kwargs)

        self.header.add_widget(CustomActionBar(title='Filtro de Clientes', current=self))
        
        self.form = FilterForm()
        self.content.add_widget(self.form)

        btn_save = Button(text='Salvar')
        btn_save.bind(on_release=self.do_save)
        
        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_release=self.do_cancel)

        buttons = BoxLayout(orientation='horizontal')
        buttons.add_widget(btn_save)
        buttons.add_widget(btn_cancel)
        self.footer.add_widget(buttons)

    def do_cancel(self, instance):
        app.sm.current = self.previous

    def do_save(self, instance):
        if self.form.save():
            app.sm.current = self.previous
