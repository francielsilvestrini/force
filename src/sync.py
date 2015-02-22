#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
data da ultima sincronizacao de cliente na configuracao
pegar todos os clientes com data de alteracao maior que a ultima sincronizacao
enviar para o servidor

pegar do servidor todas os clientes alterados apartir da data da ultima sincronizacao de cliente

'''

from datetime import datetime

from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from panellistview import PanelListView, PanelListContent, PanelListItem
from customs import CustomActionBar
from customs import AppSettings, AppUtils
from customer_form import CustomerFormScreen

from kivy.lang import Builder
Builder.load_string('''
<SyncItem>
    _status: status_label
    _desc: desc_label
    _progress: progress
    _box_labels: box_labels
    BoxLayout:
        pos: root.pos
        GridLayout:
            cols: 2
            BoxLayout:
                id: box_labels
                orientation: 'vertical'
                size_hint_x: .75
                BoxLayout:
                    orientation: 'horizontal'
                    Label:
                        text: root.title
                        font_size: '15sp'
                        text_size: self.width-10, None
                    Label:
                        id: desc_label
                        font_size: '13sp'
                        text_size: self.width-10, None
                        canvas:
                            Color:
                                rgb: .72, .72, .72
                ProgressBar:
                    id: progress
                    max: 100

            Label:
                id: status_label
                size_hint_x: .25
                markup: True
                font_size: '25sp'

<SyncMenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        CustomActionBar:
            title: 'Sincronizar com Servidor'
        GridLayout:
            cols: 1
            row_default_height: '40dp'
            row_force_default: True
            Button:
                text: 'Sincronizar Tudo'
                on_press: root.goto('sync_all')
            Button:
                text: 'Sincronizar Clientes'
                on_press: root.goto('sync_customers')
            Button:
                text: 'Sincronizar Produtos'
                on_press: root.goto('sync_products')
            Button:
                text: 'Sincronizar Pedidos'
                on_press: root.goto('sync_orders')
            Button:
                text: 'Sincronizar Tabelas'
                on_press: root.goto('sync_tables')
''');

app = App.get_running_app

class SyncListActionBar(CustomActionBar):
    def do_previous(self):
        s = self.parent.parent
        s.back_options()
        return True

class SyncItem(PanelListItem):
    title = StringProperty()
    _status = ObjectProperty(text='...')
    _desc = ObjectProperty()
    _progress = ObjectProperty()
    _box_labels = ObjectProperty()

    def process(self):
        pass

    def message_error(self, msg):
        self._status.text = 'ERRO'
        self._box_labels.add_widget(Label(text='[color=ff3333]{0}[/color]'.format(msg), markup=True))
        return

from xmlrpclib import ServerProxy
def server_connect():
    api = dict(
        hostname=app().config.get('onnixforce', 'api_hostname'),
        hostport=app().config.get('onnixforce', 'api_hostport'),
        endpoint=app().config.get('onnixforce', 'api_endpoint'))
    url = '%(hostname)s:%(hostport)s%(endpoint)s' % api
    return ServerProxy(url)


class CustomerSend(SyncItem):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', '#CLIENTES: enviar para servidor')
        kwargs.setdefault('desc', 'Aguardando...')
        super(CustomerSend, self).__init__(**kwargs)

    def process(self):
        store = JsonStore('data/customers.json')
        send_list = []
        for key in store:
            data = store[key]
            updated_on = AppUtils.strtodatetime(data['updated_on'])
            syncronized_on = AppUtils.strtodatetime(data['syncronized_on'])
            if updated_on > syncronized_on:
                send_list += [data]

        self._desc.text = {
            0:'Nenhum registro para enviar', 
            1:'Um registro para enviar', 
            2:'%s regitros para enviar'%len(send_list)}[2 if len(send_list) > 1 else len(send_list)]
        self._progress.max = len(send_list)
        self._progress.value = 0
        self._status.text = 'Enviando'
        try:
            username = app().config.get('onnixforce', 'username')

            server = server_connect()
            for data in send_list:
                self._progress.value += 1
                result = server.send_customer(username, data)
                data['syncronized_on'] = datetime.today().strftime(AppSettings.datetime_format)
                store.put(data['mobile_id'], **data)

            self._status.text = 'OK'
            return True
        except Exception, e:
            self.message_error(str(e))
            return False

class GetCustomers(SyncItem):
    def __init__(self, **kwargs):
        kwargs.setdefault('title', '#CLIENTES: atualizar do servidor')
        kwargs.setdefault('desc', 'Aguardando...')
        super(GetCustomers, self).__init__(**kwargs)

    def process(self):
        customer_update_server = app().config.get('onnixforce', 'customer_update_server')
        try:
            self._status.text = 'Conectando...'
            username = app().config.get('onnixforce', 'username')

            server = server_connect()
            result = server.get_customers(username, customer_update_server)
            customer_update_server = datetime.today().strftime(AppSettings.datetime_format)
        except Exception, e:
            self.message_error(str(e))
            return False

        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            dt_server = result['dt_server']
            print dt_server
            data_list = result['data']
            self._desc.text = {
                0:'Nenhum registro para enviar', 
                1:'Um registro para atualizar', 
                2:'%s regitros para atualizar'%len(data_list)}[2 if len(data_list) > 1 else len(data_list)]
            self._progress.max = len(data_list)
            self._progress.value = 0

            store = JsonStore('data/customers.json')
            for data_row in data_list:
                mobile_id = data_row.get('mobile_id', '')
                data = CustomerFormScreen.default_data()
                data['name'] = data_row.get('name', '')
                data['full_name'] = data_row.get('full_name', '')
                data['registry1'] = data_row.get('registry1', '')
                data['registry2'] = data_row.get('registry2', '')
                data['phone'] = data_row.get('phone', '')
                data['email'] = data_row.get('email', '')
                data['contact'] = data_row.get('contact', '')
                data['is_active'] = data_row.get('is_active', 'True')
                
                data['address'] = data_row.get('address', '')
                data['address_no'] = data_row.get('address_no', '')
                data['address_complement'] = data_row.get('address_complement', '')
                data['address_district'] = data_row.get('address_district', '')
                data['address_city'] = data_row.get('address_city', '')
                data['address_state'] = data_row.get('address_state', '')
                data['address_postal'] = data_row.get('address_postal', '')

                data['salesman'] = data_row.get('salesman', '')
                data['customer_group'] = data_row.get('customer_group', '')
                data['note'] = data_row.get('note', '')
                data['server_id'] = str(data_row.get('server_id', 0))
                data['erp_id'] = data_row.get('erp_id', '')
                if len(mobile_id) > 0:
                    data['mobile_id'] = mobile_id 
                    data['last_visit'] = data_row.get('last_visit', data['last_visit'])
                    data['visit_preferably'] = data_row.get('visit_preferably', data['visit_preferably'])
                    data['visit_info'] = data_row.get('visit_info', data['visit_info'])
                    data['next_visit'] = data_row.get('next_visit', data['next_visit'])
                else:
                    mobile_id = data['mobile_id']
                
                data['syncronized_on'] = datetime.today().strftime(AppSettings.datetime_format)
                data['updated_on'] = data['syncronized_on']

                store.put(mobile_id, **data)
                self._progress.value += 1

            self._status.text = 'OK'
            app().config.set('onnixforce', 'customer_update_server', dt_server)
            app().config.write()

            return True        
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0}\n{1}'.format(msg, msg_error))
            return False


class SyncScreen(Screen):

    def __init__(self, option, **kwargs):
        super(SyncScreen, self).__init__(name='sync', **kwargs)
        self.start(option)


    def start(self, option):
        self.option = option
        self.sync_list = []
        self.update_list()

    def do_release(self, instance):
        pass

    def back_options(self):
        sm = self.manager
        sm.current = 'sync_menu'
        return

    def update_list(self):
        content = PanelListContent()

        self.sync_list = []
        if self.option in ['sync_all', 'sync_customers', 'sync_orders']:
            item = CustomerSend()
            content.add_widget( item )
            self.sync_list += [item]

            item = GetCustomers()
            content.add_widget( item )
            self.sync_list += [item]

        view = PanelListView()
        view.add_widget(content)

        self.clear_widgets()

        layout = BoxLayout(orientation='vertical')

        actionbar = SyncListActionBar(title='Sync')
        layout.add_widget(actionbar)
        layout.add_widget(view)

        self.add_widget(layout)

        Clock.schedule_once(self.start_process, 0.6)
        return

    def start_process(self, dt):
        for item in self.sync_list:
            item.process()
        return


class SyncMenuScreen(Screen):

    #def __init__(self, name, **kwargs):
    #    super(SyncScreen, self).__init__(name=name, **kwargs)

    def goto(self, option):
        sm = self.manager
        if not sm.has_screen('sync'):
            sc = SyncScreen(option=option)
            sm.add_widget(sc)
        else:
            sc = sm.get_screen('sync')
            sc.start(option=option)
        sm.current = 'sync'
        return