from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('whatever.kv')
class MyGridLayout(Widget):

    name = ObjectProperty(None)
    color = ObjectProperty(None)
    food = ObjectProperty(None)

    def press(self):
        name = self.name.text
        color = self.color.text
        food = self.food.text

        print(f'Hello {name},you like {food} , and your favorite color is {color}!')
        #print it to the screen
        self.add_widget(Label(text =f'Hello {name},you like {food} , and your favorite color is {color}!'))
        #Clear the input boxes
        self.name.text=""
        self.color.text=""
        self.food.text=""

class TheDenizhanApp(App):
    def build(self):
        #return Label(text="Hello World",font_size =72)
        return MyGridLayout()
if __name__ == '__main__':
    TheDenizhanApp().run()