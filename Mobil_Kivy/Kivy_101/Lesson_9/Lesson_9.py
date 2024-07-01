from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


Builder.load_file('UpdateLabel.kv')
class MyLayout(Widget):
    def press(self):
        #Create variable for our widget
        name = self.ids.name_input.text
        print(name)
        #Update Label
        self.ids.name_label.text = f'Hello {name}!'
        #Clear Input Box
        self.ids.name_input.text = ''


class TheDenizhanApp(App):
    def build(self):
        #For chaning background color
        Window.clearcolor = (250/255,33/255,0,1)
        return MyLayout()
if __name__ == '__main__':
    TheDenizhanApp().run()