from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


#Set App size
Window.size = (500, 700)
Builder.load_file('Calculate.kv')
class MyLayout(Widget):
    def clear(self):
        self.ids.calc_input.text = '0'
    #Button pressing
    def button_press(self,button):
        #create variable that contains whatever text in there
        prior = self.ids.calc_input.text
        #determine if 0 is sitting  there
        if prior == "0":
            self.ids.calc_input.text = ''
            self.ids.calc_input.text = f'{button}'
        else:
            self.ids.calc_input.text = f'{prior}{button}'
    #lets create addition function
    def add(self):
        prior = self.ids.calc_input.text
        self.ids.calc_input.text = f'{prior}+'
    def subtract(self):
        prior = self.ids.calc_input.text
        self.ids.calc_input.text = f'{prior}-'
    def multiplication(self):
        prior = self.ids.calc_input.text
        self.ids.calc_input.text = f'{prior}*'
    def divide(self):
        prior = self.ids.calc_input.text
        self.ids.calc_input.text = f'{prior}/'
    def equals(self):
        prior = self.ids.calc_input.text
        #addition
        if "+"in prior:
            num_list = prior.split("+")
            answer = 0
            #loop thru our list
            for number in num_list:
                answer = answer + int(number)
            self.ids.calc_input.text = f'{answer}'
        if "-"in prior:
            num_list = prior.split("-")
            answer = 0
            #loop thru our list
            for number in num_list:
                answer = answer - int(number)
            self.ids.calc_input.text = f'{answer}'
        if "*"in prior:
            num_list = prior.split("*")
            answer = 0
            #loop thru our list
            for number in num_list:
                answer = answer * int(number)
            self.ids.calc_input.text = f'{answer}'
class CalculatorApp(App):
    def build(self):
        #For chaning background color
        Window.clearcolor = (0,0,0,1)
        return MyLayout()
if __name__ == '__main__':
    CalculatorApp().run()