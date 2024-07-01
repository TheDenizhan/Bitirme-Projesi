from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('boundedButton.kv')
class MyLayout(Widget):
   pass
class MyApp(App):
    def build(self):
        #For chaning background color
        Window.clearcolor = (1,1,1,1)
        return MyLayout()
if __name__ == '__main__':
    MyApp().run()