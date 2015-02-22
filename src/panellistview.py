#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation


from kivy.lang import Builder
Builder.load_string('''
<PanelListItem>:
    size_hint: .25, None
    height: 60
    rows: 1
    canvas:
        Color:
            rgba: 47 / 255., 167 / 255., 212 / 255., self.selected_alpha
        Rectangle:
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgb: .2, .2, .2
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

<PanelListContent>:
    cols: 1
    size_hint_y: None
''')

class PanelListItem(FloatLayout):
    selected_alpha = NumericProperty(0)
    disabled = BooleanProperty(False)

    __events__ = ('on_release', )

    def __init__(self, **kwargs):
        super(PanelListItem, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return
        touch.grab(self)
        self.selected_alpha = 1
        return super(PanelListItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            Animation(selected_alpha=0, d=.25, t='out_quad').start(self)
            self.dispatch('on_release')
            return True
        return super(PanelListItem, self).on_touch_up(touch)

    def on_release(self):
        pass


class PanelListContent(GridLayout):
    def __init__(self, **kwargs):
        super(PanelListContent, self).__init__(**kwargs)
        #layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.bind(minimum_height=self.setter('height'))


class PanelListView(ScrollView):
    pass


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout

    class SampleItem(PanelListItem):
        def __init__(self, **kwargs):
            super(SampleItem, self).__init__(**kwargs)
            content = BoxLayout(pos=self.pos)
            content.add_widget(Label(text='TITLE'))
            content.add_widget(Label(text='Description'))
            self.add_widget(content)

    class SampleApp(App):

        def build(self):
            def do_release(instance):
                print 'do_release'

            root = PanelListView()
            content = PanelListContent()

            for i in range(10):
                item = SampleItem()
                item.bind(on_release=do_release)
                content.add_widget( item )
 
            root.add_widget(content)

            return root

    SampleApp().run()