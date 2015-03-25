#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
data da ultima sincronizacao de cliente na configuracao
pegar todos os clientes com data de alteracao maior que a ultima sincronizacao
enviar para o servidor

pegar do servidor todas os clientes alterados apartir da data da ultima sincronizacao de cliente

'''

from kivy.app import App
app = App.get_running_app()

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

from widgets import MenuLayout
from widgets import HCFScreen
from actionbar import CustomActionBar
from screens import Screens
from panellistview import PanelListView
from panellistview import PanelListContent
from panellistview import PanelListItem
from messages import MessageBox
from utils import Utils

from customer_editor import CustomerForm

from datetime import datetime
import urllib
import base64

from kivy.lang import Builder
Builder.load_string('''
<SyncItemBase>
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
                GridLayout:
                    cols: 2
                    Label:
                        text: root.title
                        font_size: '15sp'
                        text_size: self.width-10, None
                        size_hint_x: .80
                    Label:
                        id: desc_label
                        size_hint_x: .20
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

''');


class MenuSyncOptions(MenuLayout):
    def __init__(self, **kwargs):
        super(MenuSyncOptions, self).__init__(**kwargs)

        info = Label(text='É RECOMENTADO AGUARDAR ATÉ A CONCLUSÃO DA'\
            +' SINCRONIZAÇÃO\nPARA UTILIZAÇÃO DO DISPOSITIVO')
        self.add_widget(info)
        
        btn = Button(text='Sincronizar Tudo')
        btn.bind(on_release=self.do_sync_all)
        self.add_widget(btn)

        btn = Button(text='Sincronizar Clientes')
        btn.bind(on_release=self.do_sync_customers)
        self.add_widget(btn)

        btn = Button(text='Sincronizar Catálogo')
        btn.bind(on_release=self.do_sync_catalog)
        self.add_widget(btn)

        btn = Button(text='Sincronizar Pedidos')
        btn.bind(on_release=self.do_sync_orders)
        self.add_widget(btn)

        btn = Button(text='Sincronizar Tabelas')
        btn.bind(on_release=self.do_sync_tables)
        self.add_widget(btn)

    def show_sync(self, option):
        sc = Screens.create('Sync')
        sc.previous = 'MenuSync'
        sc.option = option
        app.sm.current = 'Sync'
        sc.reset()

    def do_sync_all(self, instance):
        self.show_sync('sync_all')

    def do_sync_customers(self, instance):
        self.show_sync('sync_customers')

    def do_sync_catalog(self, instance):
        self.show_sync('sync_catalog')

    def do_sync_orders(self, instance):
        self.show_sync('sync_orders')

    def do_sync_tables(self, instance):
        self.show_sync('sync_tables')


class MenuSync(HCFScreen):

    def __init__(self, **kwargs):
        super(MenuSync, self).__init__(name='MenuSync', **kwargs)

        self.header.add_widget(CustomActionBar(title='Sincronizar', current=self))

        options = MenuSyncOptions()
        self.content.add_widget(options)




class SyncItemBase(PanelListItem):
    title = StringProperty()
    _status = ObjectProperty(text='...')
    _desc = ObjectProperty()
    _progress = ObjectProperty()
    _box_labels = ObjectProperty()
    
    next_process = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SyncItemBase, self).__init__(**kwargs)
        self.with_error = False

    def process(self):
        pass

    def go_next_process(self):
        if self.next_process:
            self.next_process()

    def message_error(self, msg):
        self._status.text = 'ERRO'
        if not self.with_error:
            self.with_error = True
            self._box_labels.add_widget(Label(text='[color=ff3333]{0}[/color]'.format(msg), markup=True))
            self.go_next_process()
        return

    def process_failure(self, req, result):
        self.message_error('{0} | {1}'.format('Process failure', result))
        pass

    def process_error(self, req, error):
        self.message_error('{0} | {1}'.format('Process error', error))

    def process_progress(self, req, cursize, totalsize):
        self._status.text = 'Baixando...'
        self._progress.max = totalsize
        self._progress.value = cursize

    def request_url(self, function, params):
        api = dict(
            hostname=app.config.get('onnixforce', 'api_hostname'),
            endpoint=app.config.get('onnixforce', 'api_endpoint'),
            function=function)
        url = '%(hostname)s/%(endpoint)s/api/%(function)s.json' % api

        if 'username' not in params:
            params['username'] = app.config.get('onnixforce', 'username')
        url_params = ''
        for pname in params:
            url_params += '{0}{1}={2}'.format('&' if len(url_params) > 0 else '?', pname, params[pname])
        return url + url_params

    def update_desc(self, data):
        self._desc.text = {
            0:'Nenhum registro', 
            1:'Um registro', 
            2:'%s regitros'%len(data)}[2 if len(data) > 1 else len(data)]


class SyncCities(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', '#MUNICIPIOS: atualizar do servidor')
        super(SyncCities, self).__init__(**kwargs)

    def process(self):
        states = app.config.get('onnixforce', 'states')
        states = states.replace(' ', '+')#http request
        try:
            self._status.text = 'Conectando...'

            url = self.request_url(function='cities', params=dict(states=states))

            UrlRequest(
                url=url,
                on_success=self.process_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )

            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            data = result['data']

            self.update_desc(data)

            store = app.DB.cities
            store.clear()
            for state in data:
                for row in data[state]:
                    store.put(row['code'], **row)

            self._status.text = 'OK'
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
        self.go_next_process()


class SyncCustomerGroup(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', '#GRUPO DE CLIENTES: atualizar do servidor')
        super(SyncCustomerGroup, self).__init__(**kwargs)

    def process(self):
        try:
            self._status.text = 'Conectando...'

            url = self.request_url(function='customer_groups', params=dict())

            UrlRequest(
                url=url,
                on_success=self.process_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )
            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            data = result['data']
            self.update_desc(data)

            # store = app.DB.cities
            # store.clear()
            # for state in data:
            #     for row in data[state]:
            #         store.put(row['code'], **row)

            self._status.text = 'OK'
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
        self.go_next_process()


class SyncCustomerUpdate(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'ATUALIZANDO CLIENTES: buscando no servidor')
        super(SyncCustomerUpdate, self).__init__(**kwargs)

    def process(self):
        try:
            self._status.text = 'Conectando...'

            customer_update_server = app.config.get('onnixforce', 'customer_update_server')

            url = self.request_url(function='customers', params=dict(dt=customer_update_server))

            UrlRequest(
                url=url,
                on_success=self.process_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )
            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            dt_server = result['dt_server']
            data_list = result['data']
            self.update_desc(data_list)

            store = app.DB.customers

            for data_row in data_list:
                mobile_id = data_row.get('mobile_id', '')
                data = CustomerForm.default_data()
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
                
                data['syncronized_on'] = datetime.today().strftime(Utils.datetime_format)
                data['updated_on'] = data['syncronized_on']

                store.put(mobile_id, **data)

            app.config.set('onnixforce', 'customer_update_server', dt_server)
            app.config.write()

            self._status.text = 'OK'
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
        self.go_next_process()


class SyncCustomerSend(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'ENVIANDO CLIENTES: enviando para o servidor')
        super(SyncCustomerSend, self).__init__(**kwargs)
        self.process_count = 0
        self.process_results = 0

    def data_updated(self):
        customers = app.DB.customers
        data_list = []

        for key in customers:
            record = customers[key]
            updated_on = Utils.strtodatetime(record['updated_on'])
            syncronized_on = Utils.strtodatetime(record['syncronized_on'])
            if updated_on > syncronized_on:
                data_list += [record]
        return data_list

    def process(self):
        self._status.text = 'Comparando...'
        data_list = self.data_updated()
        self.update_desc(data_list)
        self.process_count = len(data_list)
        self.process_results = 0
        if self.process_count == 0:
            self._status.text = 'OK'
            self.go_next_process()
            return True

        try:
            self._status.text = 'Enviando...'

            url = self.request_url(function='send_customer', params={})
            headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
            self._progress.max = len(data_list)
            self._progress.value = 0
            for data in data_list:
                self._progress.value += 1
                params = urllib.urlencode(data)
                req = UrlRequest(
                    url=url,
                    on_success=self.process_success,
                    on_failure=self.process_failure,
                    on_error=self.process_error,
                    req_body=params,
                    req_headers=headers,
                    )
            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_success(self, req, result):
        if result.get('code') == 100:
            mobile_id = result['data']['mobile_id']
            #server_id = result['data']['server_id']
            
            customers = app.DB.customers
            record = customers.get(mobile_id)
            record['syncronized_on'] = Utils.current_datetime_str()
            #record['server_id'] = server_id
            
            customers.put(mobile_id, **record)
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))

        self.process_results += 1
        if self.process_results == self.process_count:
            self._status.text = 'OK'
            self.go_next_process()


class SyncProductMark(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', '#MARCA DE PRODUTOS: atualizar do servidor')
        super(SyncProductMark, self).__init__(**kwargs)

    def process(self):
        try:
            self._status.text = 'Conectando...'

            url = self.request_url(function='product_mark', params=dict())

            UrlRequest(
                url=url,
                on_success=self.process_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )

            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            data_list = result['data']['marks']
            self.update_desc(data_list)

            store = app.DB.product_mark
            store.clear()
            for row in data_list:
                store.put(row['name'], **row)

            self._status.text = 'OK'
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
        self.go_next_process()


class SyncProductGroups(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', '#GRUPO DE PRODUTOS: atualizar do servidor')
        super(SyncProductGroups, self).__init__(**kwargs)

    def process(self):
        try:
            self._status.text = 'Conectando...'

            url = self.request_url(function='product_groups', params=dict())

            UrlRequest(
                url=url,
                on_success=self.process_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )

            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            data_list = result['data']['groups']
            self.update_desc(data_list)

            store = app.DB.product_groups
            store.clear()
            for row in data_list:
                store.put(row['name'], **row)

            self._status.text = 'OK'
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
        self.go_next_process()


class SyncProductUpdate(SyncItemBase):

    def __init__(self, **kwargs):
        kwargs.setdefault('title', 'PRODUTOS: buscando no servidor')
        super(SyncProductUpdate, self).__init__(**kwargs)
        self.count = 0
        self.start = 0
        self.last_update = None

    def process(self):
        try:
            self._status.text = 'Contando...'

            self.last_update = app.config.get('onnixforce', 'product_update_server')

            url = self.request_url(function='products_count', params=dict(last_update=self.last_update))

            UrlRequest(
                url=url,
                on_success=self.process_count_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )
            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_count_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Preparando...'
            self.start = 0
            self.count = result['count']
            self.process_products()
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
            self.go_next_process()


    def process_products(self):
        try:
            self._status.text = 'Conectando...'

            limitby_min = self.start
            limitby_max = self.start+100
            self.start = limitby_max

            url = self.request_url(function='products', params=dict(
                last_update=self.last_update,
                limitby_min=limitby_min,
                limitby_max=limitby_max
                ))

            UrlRequest(
                url=url,
                on_success=self.process_products_success,
                on_failure=self.process_failure,
                on_error=self.process_error,
                on_progress=self.process_progress,
                )
            return True
        except Exception, e:
            self.message_error(str(e))
            return False

    def process_products_success(self, req, result):
        if result.get('code') == 100:
            self._status.text = 'Atualizando...'
            dt_server = result['dt_server']
            data_list = result['data']['products']
            self.update_desc(data_list)

            store = app.DB.products

            for data_row in data_list:
                server_id = data_row.get('server_id', '0')
                record = {}
                record['server_id'] = server_id
                record['name'] = data_row.get('name', '')
                record['codbar'] = data_row.get('codbar', '')
                record['reference'] = data_row.get('reference', '')
                record['unit'] = data_row.get('unit', '')
                record['is_active'] = data_row.get('is_active', 'True')
                record['information'] = data_row.get('information', '')
                record['weight'] = data_row.get('weight', '')
                record['measures'] = data_row.get('measures', 'True')                
                record['max_discount'] = data_row.get('max_discount', '0.0')
                record['last_cost'] = data_row.get('last_cost', '0.0')
                record['average_cost'] = data_row.get('average_cost', '0.0')
                record['real_cost'] = data_row.get('real_cost', '0.0')
                record['default_price'] = data_row.get('default_price', '0.0')
                record['stock'] = data_row.get('stock', '0.0')
                record['erp_update'] = data_row.get('erp_update', '')
                record['erp_id'] = data_row.get('erp_id', '')
                record['mark'] = data_row.get('mark', '')
                record['group'] = data_row.get('group', '')
                record['subgroup'] = data_row.get('subgroup', '')
                record['ncm'] = data_row.get('ncm', '')
                record['taxes'] = data_row.get('taxes', [])
                record['images'] = []
                images = data_row.get('images', [])
                for image in images:
                    if len(image['base64']) == 0:
                        continue
                    image_name = 'images/{0}_{1}.jpg'.format(server_id, image['name']) 
                    jpeg_recovered = base64.decodestring(image['base64'])
                    f = open(image_name, 'w')
                    f.write(jpeg_recovered)
                    f.close()
                    record['images'] += [image_name]

                record['syncronized_on'] = datetime.today().strftime(Utils.datetime_format)
                store.put(server_id, **record)

            self._status.text = 'OK'
            if self.start > self.count:
                app.config.set('onnixforce', 'product_update_server', dt_server)
                app.config.write()
                self.go_next_process()
            else:
                self.process_products()
        else:
            msg = result.get('message')
            msg_error = result.get('error', '')
            self.message_error('{0} | {1}'.format(msg, msg_error))
            self.go_next_process()




class SyncContent(BoxLayout):
    
    option = StringProperty('')

    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        super(SyncContent, self).__init__(**kwargs)
        self.items = []

        self.view = PanelListView()
        self.add_widget(self.view)        
        #self.reset()

    def reset(self):
        self.view.clear_widgets()
        content = PanelListContent()
        if self.option in ['sync_tables']:
            item = SyncCities()
            content.add_widget(item)
            self.items += [item]

            # item = SyncCustomerGroup()
            # content.add_widget(item)
            # self.items += [item]

            item = SyncProductMark()
            content.add_widget(item)
            self.items += [item]

            item = SyncProductGroups()
            content.add_widget(item)
            self.items += [item]


        if self.option in ['sync_customers', 'sync_all']:
            item = SyncCustomerSend()
            content.add_widget(item)
            self.items += [item]

            item = SyncCustomerUpdate()
            content.add_widget(item)
            self.items += [item]

        if self.option in ['sync_catalog', 'sync_all']:
            item = SyncProductUpdate()
            content.add_widget(item)
            self.items += [item]

        
        self.view.add_widget(content)
       
        Clock.schedule_once(self.start_process, 1.0)
        
    def start_process(self, dt):
        for i, item in enumerate(self.items):
            if i > 0:
                self.items[i-1].next_process = item.process
        self.items[-1].next_process = self.do_sync_complete
        self.items[0].process()

    def do_sync_complete(self):
        MessageBox(text='Sincronização concluída!')


class Sync(HCFScreen):

    option = StringProperty('')

    def __init__(self, **kwargs):
        super(Sync, self).__init__(name='Sync', **kwargs)

        self.header.add_widget(CustomActionBar(title='Sincronizar', current=self))

        self.synccontent = SyncContent()
        self.content.add_widget(self.synccontent)

        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_release=self.do_cancel)
        self.footer.add_widget(btn_cancel)
        #self.reset()

    def reset(self):
        self.synccontent.option = self.option
        self.synccontent.reset()

    def do_cancel(self, instance):
        app.sm.current = self.previous
