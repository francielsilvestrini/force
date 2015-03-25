#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
app = App.get_running_app()

from kivy.factory import Factory

class Screens(object):
    @staticmethod
    def create(name):
        if not app.sm.has_screen(name):
            cls = Factory.get(name)
            sc = cls()
            app.sm.add_widget(sc)
        else:
            sc = app.sm.get_screen(name)
        return sc

    @staticmethod
    def create_and_show(name):
        sc = Screens.create(name)
        sc.reset()
        app.sm.current = name
        return sc
