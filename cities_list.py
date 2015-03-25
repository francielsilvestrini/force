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

from actionbar import CustomActionBar
from customs import CustomTextInput
from widgets import FormLayout
from widgets import HCFScreen
from widgets import SearchLayout
from panellistview import PanelListView
from panellistview import PanelListContent
from panellistview import PanelListItem


from kivy.lang import Builder
Builder.load_string('''
<CitiesListItem>
    height: 40
    BoxLayout:
        pos: root.pos
        Label:
            size_hint_x: .75
            text: root.name
            font_size: '15sp'
            text_size: self.width-10, None
        Label:
            size_hint_x: .25
            text: root.state
            font_size: '15sp'
            text_size: self.width-10, None,
''');


class SearchCities(SearchLayout):

    __events__ = ('on_search', )

    def __init__(self, **kwargs):
        super(SearchCities, self).__init__(**kwargs)
        self.field = Button(text='Nome', size_hint=(.15, 1))
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


class CitiesListItem(PanelListItem):
    name = StringProperty()
    state = StringProperty()


class CitiesListContent(BoxLayout):
    
    state = StringProperty()
    selected = ObjectProperty(None, allownone=True)

    __events__ = ('on_item_selected', )

    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        super(CitiesListContent, self).__init__(**kwargs)

        search = SearchCities()
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
            content.add_widget(CitiesListItem())
            self.view.add_widget(content)

    def do_search(self, instance):
        self.reset(with_default=False)
        content = PanelListContent()
        cities = app.DB.cities
        for key in cities:
            row = cities[key]
            if row['state'] != self.state:
                continue

            if len(instance.content.text) > 0 \
            and instance.content.text.upper() in row['name']:
                item = CitiesListItem(name=row['name'], state=row['state'])
                item.bind(on_release=self.do_select_item)
                content.add_widget(item)

        if len(content.children) == 0:
            item = CitiesListItem(name='<Nenhum Municípios Localizado>')
            content.add_widget(item)
        self.view.add_widget(content)

    def do_select_item(self, instance):
        self.selected = instance
        self.dispatch('on_item_selected')

    def on_item_selected(self):
        pass

class CitiesList(HCFScreen):

    state = StringProperty()
    item_selected = ObjectProperty(None, allownone=True)

    __events__ = ('on_selected', )

    def __init__(self, **kwargs):
        super(CitiesList, self).__init__(name='CitiesList', **kwargs)

        self.header.add_widget(CustomActionBar(title='Municípios', current=self))

        self.citiescontent = CitiesListContent()
        self.citiescontent.bind(on_item_selected=self.do_item_selected)
        self.content.add_widget(self.citiescontent)

        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_release=self.do_cancel)
        self.footer.add_widget(btn_cancel)
        self.reset()

    def reset(self):
        self.item_selected = None
        self.citiescontent.state = self.state
        self.citiescontent.reset()

    def do_cancel(self, instance):
        app.sm.current = self.previous

    def do_item_selected(self, instance):
        self.item_selected = instance.selected
        self.dispatch('on_selected')

    def on_selected(self):
        pass
