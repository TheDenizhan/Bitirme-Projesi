from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.slider import Slider
Builder.load_file('sliders.kv')
class MyLayout(Widget):
   def slide_it(self,*args):
       print(*args)
       self.slide_text.text=str(int(args[1]))
       self.slide_text.font_size=str(int(args[1])*10)

class MyApp(App):
    def build(self):
        #For chaning background color
        Window.clearcolor = (0,0,0,1)
        return MyLayout()
if __name__ == '__main__':
    MyApp().run()