#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

from kivy.lang import Builder
Builder.load_string('''
<CustomTextInput>
    multiline: False
    write_tab: False
''');


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

    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        return super(CustomTextInput, self).insert_text(s, from_undo=from_undo)



class FloatInput(CustomTextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.',1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class DateInput(CustomTextInput):
    def insert_text(self, substring, from_undo=False):
        return super(DateInput, self).insert_text(s, from_undo=from_undo)
