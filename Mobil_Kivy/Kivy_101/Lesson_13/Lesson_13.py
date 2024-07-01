from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.slider import Slider
Builder.load_file('accordions.kv')
class MyLayout(Widget):
    pass

class MyApp(App):
    def build(self):
        #For chaning background color
        Window.clearcolor = (0,0,0,1)
        return MyLayout()
if __name__ == '__main__':
    MyApp().run()