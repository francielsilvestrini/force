#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from datetime import datetime

from kivy.uix.actionbar import ActionBar
from kivy.uix.textinput import TextInput

from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_string('''
<CustomActionBar>:
    pos_hint: {'top':1}
    ActionView:
        use_separator: True
        ActionPrevious:
            title: root.title
            with_previous: False
            on_press: root.do_previous()
        ActionGroup:
            ActionButton:
                text: ':)'
                on_press: root.do_customer()
            ActionButton:
                text: '[0]'
                on_press: root.do_order()
            ActionButton:
                text: 'Sair'
                on_press: root.do_close()

<CustomTextInput>
    multiline: False
    write_tab: False
''');


class AppSettings(object):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    date_format = '%Y-%m-%d'

class AppUtils(object):
    @staticmethod
    def strtodatetime(datetime_str):
        datetime_str = datetime_str.replace(' ', '-')
        datetime_str = datetime_str.replace(':', '-')
        dt_list = datetime_str.split('-')

        fmt = AppSettings.datetime_format.replace(' ', '-')
        fmt = fmt.replace(':', '-')
        fmt = fmt.replace('%', '')
        fmt_list = fmt.split('-')

        d = {}
        for i, k in enumerate(fmt_list):
            d[k] = int(dt_list[i])

        return datetime(d['Y'], d['m'], d['d'], d['H'], d['M'], d['S'])


class CustomActionBar(ActionBar):

    title = StringProperty('')

    def __init__(self, **kwargs):
        super(CustomActionBar, self).__init__(**kwargs)

    def do_previous(self):
        sm = self.parent.parent.manager
        sm.current = 'menu'
        return True

    def do_close(self):
        app = App.get_running_app()
        app.stop()

    def do_customer(self):
        pass
    def do_order(self):
        pass


class CustomTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        self.next = kwargs.get('next', None)
        super(CustomTextInput, self).__init__(*args, **kwargs)
    
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, key_str = keycode
        if key in (9,13) and self.next is not None:
            self.next.focus = True
            self.next.select_all()
        else:
            super(CustomTextInput, self)._keyboard_on_key_down( \
                window, keycode, text, modifiers)


class FloatInput(CustomTextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.',1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)