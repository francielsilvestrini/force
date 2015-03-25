#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app()

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty

from actionbar import CustomActionBar
from customs import CustomTextInput
from widgets import FormLayout
from widgets import HCFScreen
from widgets import SearchLayout
from panellistview import PanelListView
from panellistview import PanelListContent
from panellistview import PanelListItem
from screens import Screens


from kivy.lang import Builder
Builder.load_string('''
<ProductsListItem>
    BoxLayout:
        pos: root.pos
        GridLayout:
            cols: 1
            GridLayout:
                cols: 2

                Label:
                    size_hint_x: .75
                    markup: True
                    text: u'{0}[size=13sp][color=999999]  {1}[/color][/size]'.format(root.data['name'], root.data['default_price'])
                    font_size: '15sp'
                    text_size: self.width-10, None
                Label:
                    size_hint_x: .25
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Cod.Bar.', root.data.get('codbar') or '')
                    font_size: '15sp'
                    text_size: self.width-10, None,

            GridLayout:
                cols: 3

                Label:
                    size_hint_x: .20
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Grupo', root.data.get('group') or '')
                    font_size: '15sp'
                    text_size: self.width-10, None
                Label:
                    size_hint_x: .30
                    markup: True
                    text: u'{0}'.format(root.data.get('subgroup','') )
                    font_size: '15sp'
                    text_size: self.width-10, None
                Label:
                    size_hint_x: .25
                    markup: True
                    text: u'[size=13sp][color=999999]{0}[/color][/size] {1}'.format('Marca', root.data.get('mark','') )
                    font_size: '15sp'
                    text_size: self.width-10, None

                    
                Button:
                    size_hint_x: .25
                    text: u'Detalhar'
''');


class SearchProduct(SearchLayout):

    __events__ = ('on_search', )

    def __init__(self, **kwargs):
        super(SearchProduct, self).__init__(**kwargs)
        self.field = Button(text='Identif.', size_hint=(.15, 1))
        self.filter_type = Button(text='Contendo', size_hint=(.15, 1))
        self.content = CustomTextInput()
        search = Button(text='Localizar', size_hint=(.15, 1))
        search.bind(on_release=self.do_search)

        self.add_widget(self.field)
        self.add_widget(self.filter_type)
        self.add_widget(self.content)
        self.add_widget(search)

    def do_search(self, instance):
        self.dispatch('on_search')

    def on_search(self):
        pass


class ProductsListItem(PanelListItem):
    key = StringProperty()
    data = DictProperty(None)


class ProductsListContent(BoxLayout):
    
    selected = ObjectProperty(None, allownone=True)

    __events__ = ('on_item_selected', )

    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        super(ProductsListContent, self).__init__(**kwargs)

        search = SearchProduct()
        search.bind(on_search=self.do_search)
        self.add_widget(search)
        self.view = PanelListView()
        self.add_widget(self.view)        
        self.reset()

    def reset(self, with_default=True):
        self.selected = None
        self.view.clear_widgets()
        if with_default:
            #but, scrollview sem conteudo da erro
            content = PanelListContent()
            content.add_widget(PanelListItem())
            self.view.add_widget(content)

    def do_search(self, instance):
        self.reset(with_default=False)
        content = PanelListContent()

        # customer_filter = app.DB.preferences.get('customer_filter')
        # filter_state = lambda x: x == customer_filter['state'] or customer_filter['state'] == app.DB.select_text
        # filter_city = lambda x: x == customer_filter['city'] or customer_filter['city'] == app.DB.select_text

        products = app.DB.products
        for key in products:
            row = products[key]

            # if not filter_state(row['address_state']) or not filter_city(row['address_city']):
            #     continue

            if len(instance.content.text) > 0 \
            and instance.content.text.upper() in row['name'].upper():
                item = ProductsListItem(key=key, data=row)
                item.bind(on_release=self.do_select_item)
                content.add_widget(item)

        if len(content.children) == 0:
            item = PanelListItem(name='<Nenhum Produto Localizado>')
            content.add_widget(item)
        self.view.add_widget(content)

    def do_select_item(self, instance):
        self.selected = instance
        self.dispatch('on_item_selected')

    def on_item_selected(self):
        pass

class ProductsList(HCFScreen):

    item_selected = ObjectProperty(None, allownone=True)

    __events__ = ('on_selected', )

    def __init__(self, **kwargs):
        super(ProductsList, self).__init__(name='ProductsList', **kwargs)

        self.header.add_widget(CustomActionBar(title='Produtos', current=self))

        self.productscontent = ProductsListContent()
        self.productscontent.bind(on_item_selected=self.do_item_selected)
        self.content.add_widget(self.productscontent)

        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_release=self.do_cancel)
        self.footer.add_widget(btn_cancel)
        self.reset()

    def reset(self):
        self.item_selected = None
        self.productscontent.reset()

    def do_cancel(self, instance):
        app.sm.current = self.previous

    def do_item_selected(self, instance):
        # if self.previous == 'Menu':
        #     sc = Screens.create('CustomerEditor')
        #     sc.previous = 'ProductsList'
        #     sc.record_key = instance.selected.key
        #     sc.reset()
        #     app.sm.current = 'CustomerEditor'
        # else:
        #     self.item_selected = instance.selected
        #     self.dispatch('on_selected')
        pass

    def on_selected(self):
        pass
