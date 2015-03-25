#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform

class DataJson(object):
    select_text = 'Selecionar...'

    def __init__(self, **kwargs):
        super(DataJson, self).__init__(**kwargs)
        self.cities = None
        self.preferences = None

    def start(self):
        print platform()
        #if PLATFORM in ('windows','linux','osx'):
        #    self._app_window.size = 400,600

        self.cities = JsonStore(join('data','cities.json'))    
        self.preferences = JsonStore(join('data','preferences.json'))
        self.customers = JsonStore(join('data','customers.json'))
        self.product_mark = JsonStore(join('data','product_mark.json'))
        self.product_groups = JsonStore(join('data','product_groups.json'))
        self.products = JsonStore(join('data','products.json'))
        self.load_preferences()

    def load_preferences(self):
        if self.preferences.exists('customer_filter'):
            row = self.preferences['customer_filter']
        else:
            row = {}
        if 'state' not in row:
            row['state'] = self.select_text
        if 'city' not in row:
            row['city'] = self.select_text
        self.preferences.put('customer_filter', **row)
