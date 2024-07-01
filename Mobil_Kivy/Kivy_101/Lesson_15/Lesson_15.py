from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.slider import Slider
Builder.load_file('checkbox.kv')
class MyLayout(Widget):
    def checkbox_click(self,instance,value):
        print("Check",value)

class MyApp(App):
    def build(self):
        return MyLayout()
if __name__ == '__main__':
    MyApp().run()