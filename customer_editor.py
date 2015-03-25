#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app()

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.properties import StringProperty

from customs import CustomTextInput
from customs import DateInput
from widgets import HCFScreen
from widgets import FormLayout
from actionbar import CustomActionBar
from messages import MessageBoxContent
from utils import Utils
from customer_filter import StateSelect
from screens import Screens

from collections import OrderedDict
import uuid


def default_state():
    preferences = app.DB.preferences
    value = preferences.get('customer_filter')['state']   
    if value == app.DB.select_text:
        return ''
    else:
        return value

def default_city():
    preferences = app.DB.preferences
    value = preferences.get('customer_filter')['city']   
    if value == app.DB.select_text:
        return ''
    else:
        return value

def default_postal():
    return ''

customer_schema = {
    'name': {
        'type': 'string', 
        'label': 'Nome', 
        'default': '', 
        'required': True,
        },
    'full_name': {
        'type': 'string', 
        'label': 'Razão Social', 
        'default': '',
        'required': True,
        },
    'registry1': {
        'type': 'string', 
        'label': 'CNPJ', 
        'default': '',
        'required': True,
        },
    'registry2': {
        'type': 'string', 
        'label': 'IE', 
        'default': '', 
        },
    'phone': {
        'type': 'string', 
        'label': 'Telefone', 
        'default': '', 
        'required': True,
        },
    'email': {
        'type': 'string', 
        'label': 'Email', 
        'default': '', 
        },
    'contact': {
        'type': 'string', 
        'label': 'Contato', 
        'default': '', 
        },
    'is_active': {
        'type': 'boolean', 
        'label': 'Situação', 
        'default': 'True', 
        },
            
    'address': {
        'type': 'string', 
        'label': 'Endereço', 
        'default': '', 
        },
    'address_no': {
        'type': 'string', 
        'label': 'Numero', 
        'default': '', 
        },
    'address_complement': {
        'type': 'string', 
        'label': 'Complemento', 
        'default': '', 
        },
    'address_district': {
        'type': 'string', 
        'label': 'Bairro', 
        'default': '', 
        },
    'address_state': {
        'type': 'state', 
        'label': 'Estado', 
        'default': default_state,
        'required': True, 
        },
    'address_city': {
        'type': 'city', 
        'label': 'Município', 
        'default': default_city, 
        'required': True,
        },
    'address_postal': {
        'type': 'string', 
        'label': 'CEP', 
        'default': default_postal, 
        },

    'salesman': {
        'type': 'string', 
        'label': 'Vendedor', 
        'default': app.config.get('onnixforce', 'username'),
        'readonly': True,
        },
    'customer_group': {
        'type': 'string', 
        'label': 'Grupo', 
        'default': '', 
        },
    'note': {
        'type': 'string', 
        'label': 'Observação', 
        'default': '', 
        },
    'server_id': {
        'type': 'string', 
        'label': 'Id Servidor', 
        'default': '0', 
        'readonly': True,
        },
    'mobile_id': {
        'type': 'string', 
        'label': 'Id', 
        'default': uuid.uuid4, 
        'readonly': True,
        },
    'erp_id': {
        'type': 'string', 
        'label': 'Id ERP', 
        'default': '', 
        'readonly': True,
        },
            
    'last_visit': {
        'type': 'date', 
        'label': 'Ultima Visita', 
        'default': Utils.current_date_str, 
        },
    'visit_preferably': {
        'type': 'string', 
        'label': 'Preferencia de Visita', 
        'default': '', 
        },
    'visit_info': {
        'type': 'string', 
        'label': 'Informações', 
        'default': '', 
        },
    'next_visit': {
        'type': 'date', 
        'label': 'Próxima Visita', 
        'default': Utils.current_date_str, 
        },
    'syncronized_on': {
        'type': 'string', 
        'label': 'Sincronizado em', 
        'default': Utils.current_datetime_str, 
        'readonly': True,
        },
    'updated_on': {
        'type': 'string', 
        'label': 'Alterado em', 
        'default': Utils.current_datetime_str, 
        'readonly': True,
        },
}


class CustomerForm(BoxLayout):
    def __init__(self, **kwargs):
        super(CustomerForm, self).__init__(**kwargs)
        self.is_new_record = True
        self.widgets = {}
        for name in customer_schema:
            if customer_schema[name]['type'] == 'boolean':
                self.widgets[name] = Switch()
            elif customer_schema[name]['type'] == 'date':
                self.widgets[name] = DateInput()
            elif customer_schema[name]['type'] == 'state':
                self.widgets[name] = StateSelect()
                self.widgets[name].bind(on_update=self.do_update_select)                
            elif customer_schema[name]['type'] == 'city':
                preferences = app.DB.preferences
                self.widgets[name] = Button(text=preferences.get('customer_filter')['city'])
                self.widgets[name].bind(on_release=self.select_city)                
            else:
                props = {'readonly': customer_schema[name].get('readonly', False)}
                self.widgets[name] = CustomTextInput(**props)

        tab_items = OrderedDict()
        tab_items['Identificação'] = ['name', 'full_name', 'registry1',\
            'registry2', 'phone', 'email', 'contact', 'is_active']
        tab_items['Endereço'] = ['address', 'address_no', 'address_complement',\
            'address_district','address_state', 'address_city', 'address_postal']
        tab_items['Adicional'] = ['salesman', 'customer_group', 'note', \
            'server_id', 'mobile_id', 'erp_id', 'syncronized_on', 'updated_on']
        tab_items['Visita'] = ['last_visit', 'visit_preferably', 'visit_info', \
            'next_visit']

        tp = TabbedPanel(**{'do_default_tab':False})
        for k in tab_items:
            layout = FormLayout()
            for fname in tab_items[k]:
                layout.add_widget(Label(text=customer_schema[fname]['label']))
                layout.add_widget(self.widgets[fname])
            ti = TabbedPanelItem(text=k)
            ti.add_widget(layout)
            tp.add_widget(ti)
        self.add_widget(tp)

    def do_update_select(self, instance):
        self.widgets['address_city'].text = app.DB.select_text

    def select_city(self, instance):
        state = self.widgets['address_state']
        if state.text == app.DB.select_text:
            MessageBox(text='Selecione um estado!')
            return
        sc = Screens.create('CitiesList')
        sc.previous = 'CustomerEditor'
        if sc.state != state.text:
            sc.state = state.text
            sc.reset()
        sc.bind(on_selected=self.do_selected_city)
        app.sm.current = 'CitiesList'

    def do_selected_city(self, instance):
        self.widgets['address_city'].text = instance.item_selected.name
        app.sm.current = 'CustomerEditor'

    @staticmethod
    def default_data():
        data = {}
        for fname in customer_schema:
            default = customer_schema[fname]['default']
            if callable(default):
                value = default()
            else:
                value = default
            data[fname] = str(value)
        return data

    def load(self, key):
        self.is_new_record = True
        data = self.default_data()

        if app.DB.customers.exists(key):
            self.is_new_record = False
            row = app.DB.customers.get(key)
            #update schema
            for k in data:
                data[k] = row.get(k, data[k])

        for fname in customer_schema:
            if customer_schema[fname]['type'] == 'boolean':
                self.widgets[fname].active = data[fname] == 'True'
            else:
                self.widgets[fname].text = data[fname]

    def widget_value(self, fname):
        if customer_schema[fname]['type'] == 'boolean':
            return 'True' if self.widgets[fname].active else 'False'
        else:
            return self.widgets[fname].text

    def validate(self):
        requireds = []
        for fname in customer_schema:
            is_required = customer_schema[fname].get('required', False)
            if not is_required:
                continue
            value = self.widget_value(fname)
            if len(value.strip()) == 0:
                requireds += [customer_schema[fname]['label']]

        if len(requireds) > 0:
            content = BoxLayout(orientation='vertical')
            for s in requireds:
                content.add_widget(Label(text='-'+s))
            MessageBoxContent(content=content, title='Campos requeridos...')
            return False
        else:
            return True

    def save(self):
        if not self.validate():
            return False

        record = {}
        for fname in customer_schema:
            value = self.widget_value(fname)
            record[fname] = str(value)
        record['updated_on'] = Utils.current_datetime_str()

        customers = app.DB.customers
        customers.put(record['mobile_id'], **record)
        return True


class CustomerEditor(HCFScreen):

    record_key = StringProperty('')

    def __init__(self, **kwargs):
        super(CustomerEditor, self).__init__(name='CustomerEditor', **kwargs)

        self.header.add_widget(CustomActionBar(title='Cliente', current=self))
        
        self.form = CustomerForm()
        self.content.add_widget(self.form)

        btn_save = Button(text='Salvar')
        btn_save.bind(on_release=self.do_save)
        
        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_release=self.do_cancel)

        buttons = BoxLayout(orientation='horizontal')
        buttons.add_widget(btn_save)
        buttons.add_widget(btn_cancel)
        self.footer.add_widget(buttons)
        self.reset()

    def do_cancel(self, instance):
        app.sm.current = self.previous

    def do_save(self, instance):
        if self.form.save():
            if self.previous == 'CustomerList':
                sc = app.sm.get_screen('CustomerList')
                sc.reset()
            app.sm.current = self.previous

    def reset(self):
        self.form.load(self.record_key)

