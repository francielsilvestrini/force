#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app()

from kivy.uix.actionbar import ActionBar

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from kivy.lang import Builder
Builder.load_string('''
<CustomActionBar>:
    pos_hint: {'top':1}
    ActionView:
        use_separator: True
        ActionPrevious:
            title: root.title
            with_previous: root.current != None
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
''');



class CustomActionBar(ActionBar):

    title = StringProperty('')
    current = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CustomActionBar, self).__init__(**kwargs)

    def do_previous(self):
        previous = 'Menu'
        if self.current and self.current.previous:
            previous = self.current.previous
        app.sm.current = previous
        return True

    def do_close(self):
        app.stop()

    def do_customer(self):
        pass
    def do_order(self):
        pass
