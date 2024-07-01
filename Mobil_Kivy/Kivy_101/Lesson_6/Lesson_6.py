from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
Builder.load_file('inherit.kv')
class MyLayout(Widget):
    pass


class TheDenizhanApp(App):
    def build(self):
        #For chaning background color 
        Window.clearcolor = (1,1,1,1)
        #return Label(text="Hello World",font_size =72)
        return MyLayout()
if __name__ == '__main__':
    TheDenizhanApp().run()