from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('box.kv')
class MyLayout(Widget):
    pass


class TheDenizhanApp(App):
    def build(self):
        #return Label(text="Hello World",font_size =72)
        return MyLayout()
if __name__ == '__main__':
    TheDenizhanApp().run()