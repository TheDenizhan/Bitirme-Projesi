from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


Builder.load_file('FloatLayout.kv')
class MyLayout(Widget):
    pass


class TheDenizhanApp(App):
    def build(self):
        #For chaning background color
        Window.clearcolor = (250/255,33/255,0,1)
        return MyLayout()
if __name__ == '__main__':
    TheDenizhanApp().run()