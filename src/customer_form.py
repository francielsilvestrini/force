#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore

from customs import AppSettings
from customs import CustomActionBar
from customs import CustomTextInput

Builder.load_string('''
<CustomerFormScreen>:
    _name: name_input
    _full_name: full_name_input
    _registry1: registry1_input
    _registry2: registry2_input
    _phone: phone_input
    _email: email_input
    _contact: contact_input
    _is_active: is_active_input

    _address: address_input
    _address_no: address_no_input
    _address_complement: address_complement_input
    _address_district: address_district_input
    _address_city: address_city_input
    _address_state: address_state_input
    _address_postal: address_postal_input

    _salesman: salesman_input
    _customer_group: customer_group_input
    _note: note_input
    _mobile_id: mobile_id_input
    _server_id: server_id_input
    _erp_id: erp_id_input

    _last_visit: last_visit_input
    _visit_preferably: visit_preferably_input
    _visit_info: visit_info_input
    _next_visit: next_visit_input

    BoxLayout:
        orientation: 'vertical'
        CustomActionBar:
            title: 'Novo Cliente'

        TabbedPanel:
            do_default_tab: False
            TabbedPanelItem:
                text: 'Identificação'
                ScrollView:
                    GridLayout:
                        cols: 2
                        spacing: 10
                        padding: 20
                        row_default_height: '40dp'
                        row_force_default: True
                        Label:
                            text: 'Nome Fantasia'
                        CustomTextInput:
                            id: name_input
                            focused: True
                        Label:
                            text: 'Razão Social'
                        CustomTextInput:
                            id: full_name_input
                        Label:
                            text: 'CNPJ'
                        CustomTextInput:
                            id: registry1_input
                        Label:
                            text: 'IE'
                        CustomTextInput:
                            id: registry2_input
                        Label:
                            text: 'Telefone'
                        CustomTextInput:
                            id: phone_input
                        Label:
                            text: 'Email'
                        CustomTextInput:
                            id: email_input
                        Label:
                            text: 'Contato'
                        CustomTextInput:
                            id: contact_input
                        Label:
                            text: 'Situação'
                        Switch:
                            id: is_active_input

            TabbedPanelItem:
                text: 'Endereço'
                ScrollView:
                    GridLayout:
                        cols: 2
                        spacing: 10
                        padding: 20
                        row_default_height: '40dp'
                        row_force_default: True
                        Label:
                            text: 'Rua'
                        CustomTextInput:
                            id: address_input
                        Label:
                            text: 'Numero'
                        CustomTextInput:
                            id: address_no_input
                        Label:
                            text: 'Complemento'
                        CustomTextInput:
                            id: address_complement_input
                        Label:
                            text: 'Bairro'
                        CustomTextInput:
                            id: address_district_input
                        Label:
                            text: 'Município'
                        CustomTextInput:
                            id: address_city_input
                        Label:
                            text: 'Estado'
                        CustomTextInput:
                            id: address_state_input
                        Label:
                            text: 'CEP'
                        CustomTextInput:
                            id: address_postal_input

            TabbedPanelItem:
                text: 'Adicional'
                ScrollView:
                    GridLayout:
                        cols: 2
                        spacing: 10
                        padding: 20
                        row_default_height: '40dp'
                        row_force_default: True
                        Label:
                            text: 'Vendedor'
                        CustomTextInput:
                            id: salesman_input
                        Label:
                            text: 'Grupo'
                        CustomTextInput:
                            id: customer_group_input
                        Label:
                            text: 'Observação'
                        TextInput:
                            id: note_input
                        Label:
                            text: 'Id Local'
                        CustomTextInput:
                            id: mobile_id_input
                            readonly: True
                        Label:
                            text: 'Id no Servidor'
                        CustomTextInput:
                            id: server_id_input
                            readonly: True
                        Label:
                            text: 'Id ERP'
                        CustomTextInput:
                            id: erp_id_input
                            readonly: True

            TabbedPanelItem:
                text: 'Visita'
                ScrollView:
                    GridLayout:
                        cols: 2
                        spacing: 10
                        padding: 20
                        row_default_height: '40dp'
                        row_force_default: True

                        Label:
                            text: 'Ultima Visita'
                        CustomTextInput:
                            id: last_visit_input
                        Label:
                            text: 'Preferencia para Visita'
                        TextInput:
                            id: visit_preferably_input
                            minimun_height: '60dp'
                        Label:
                            text: 'Informações'
                        TextInput:
                            id: visit_info_input
                        Label:
                            text: 'Próxima Visita'
                        CustomTextInput:
                            id: next_visit_input

        BoxLayout:
            size_hint: (1,None)
            size: (1,40)
            orientation: "horizontal"
            Button:
                text: 'Salvar'
                on_press: root.do_save()
            Button:
                text: 'Cancelar'
                on_press: root.do_cancel()


''');
app = App.get_running_app

class CustomerFormScreen(Screen):
    _name = ObjectProperty()
    _full_name = ObjectProperty()
    _registry1 = ObjectProperty()
    _registry2 = ObjectProperty()
    _phone = ObjectProperty()
    _email = ObjectProperty()
    _contact = ObjectProperty()
    _is_active = ObjectProperty()

    _address = ObjectProperty()
    _address_no = ObjectProperty()
    _address_complement = ObjectProperty()
    _address_district = ObjectProperty()
    _address_city = ObjectProperty()
    _address_state = ObjectProperty()
    _address_postal = ObjectProperty()

    _salesman = ObjectProperty()
    _customer_group = ObjectProperty()
    _note = ObjectProperty()
    _server_id = ObjectProperty()
    _mobile_id = ObjectProperty()
    _erp_id = ObjectProperty()

    _last_visit = ObjectProperty()
    _visit_preferably = ObjectProperty()
    _visit_info = ObjectProperty()
    _next_visit = ObjectProperty()

    key = StringProperty(None)

    def __init__(self, name, **kwargs):
        super(CustomerFormScreen, self).__init__(name=name, **kwargs)

        self.fields = {
            'name': self._name,
            'full_name': self._full_name,
            'registry1': self._registry1,
            'registry2': self._registry2,
            'phone': self._phone,
            'email': self._email,
            'contact': self._contact,
            'is_active': self._is_active,
            'address': self._address,
            'address_no': self._address_no,
            'address_complement': self._address_complement,
            'address_district': self._address_district,
            'address_city': self._address_city,
            'address_state': self._address_state,
            'address_postal': self._address_postal,
            'salesman': self._salesman,
            'customer_group': self._customer_group,
            'note': self._note,
            'server_id': self._server_id,
            'mobile_id': self._mobile_id,
            'erp_id': self._erp_id,
            'last_visit': self._last_visit,
            'visit_preferably': self._visit_preferably,
            'visit_info': self._visit_info,
            'next_visit': self._next_visit,
        }
        self.record = {}
        self.load_data()
        return

    def load_data(self):
        if self.key is None:
            self.record = CustomerFormScreen.default_data()
        else:
            store = JsonStore('data/customers.json')
            self.record = store[self.key]

        for fname in self.fields:
            if self.record.get(fname, None) is not None:
                field = self.fields[fname]
                if fname in['is_active']:
                    field.active = self.record[fname]=='True'
                else:
                    field.text = self.record[fname]
        return

    def back_screen(self):
        sm = self.manager
        sm.current = 'menu'
        return

    def do_save(self):
        for fname in self.fields:
            field = self.fields[fname]
            if fname in['is_active']:
                self.record[fname] = 'True' if field.active else 'False'
            else:
                self.record[fname] = field.text
        self.record['updated_on'] = datetime.today().strftime(AppSettings.datetime_format)

        store = JsonStore('data/customers.json')
        store.put(self.record['mobile_id'], **self.record)

        self.back_screen()
        return

    def do_cancel(self):
        self.back_screen()
        return

    @staticmethod
    def default_data():
        data = {
            'name': '',
            'full_name': '',
            'registry1': '',
            'registry2': '',
            'phone': '',
            'email': '',
            'contact': '',
            'is_active': 'True',
            
            'address': '',
            'address_no': '',
            'address_complement': '',
            'address_district': '',
            'address_city': '',
            'address_state': '',
            'address_postal': '',

            'salesman': app().config.get('onnixforce', 'username'),
            'customer_group': '',
            'note': '',
            'server_id': '0',
            'mobile_id': str(uuid.uuid4()),
            'erp_id': '',
            
            'last_visit': datetime.today().strftime(AppSettings.date_format),
            'visit_preferably': '',
            'visit_info': '',
            'next_visit': datetime.today().strftime(AppSettings.date_format),            

            'syncronized_on': datetime.today().strftime(AppSettings.datetime_format),
            }
        data['updated_on'] = data['syncronized_on']
        return data