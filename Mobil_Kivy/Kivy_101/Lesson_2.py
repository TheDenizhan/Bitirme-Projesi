import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyGridLayout(GridLayout):
    #Initialize infinite keywords
    def __init__(self,**kwargs):
        #call grid layout constructor
        super(MyGridLayout,self).__init__(**kwargs)
        #set columns
        self.cols = 1
        self.row_force_default = True
        self.row_default_height =120
        self.col_force_default = True
        self.col_default_width = 500
        #create second layout
        self.top_grid = GridLayout(
            row_force_default =True,
            row_default_height=40,
            col_force_default = True,
            col_default_width =200
        )
        self.top_grid.cols = 2
        #add widgets
        self.top_grid.add_widget(Label(text= "Name: "))
        #add input box
        self.name = TextInput(multiline = False)
        self.top_grid.add_widget(self.name)
        # add widgets
        self.top_grid.add_widget(Label(text="Favorite Color: "))
        # add input box
        self.color = TextInput(multiline=False)
        self.top_grid.add_widget(self.color)
        # add widgets
        self.top_grid.add_widget(Label(text="Favorite Food: "))
        # add input box
        self.food = TextInput(multiline=False)
        self.top_grid.add_widget(self.food)
        #add the new top_grid to our app
        self.add_widget(self.top_grid)
        #Create a submit Button
        self.submit = Button(text = "Submit",
                             font_size= 32,
                             size_hint_y =None,
                             height=50,
                             size_hint_x =None,
                             width =200)
        self.submit.bind(on_press= self.press)
        self.add_widget(self.submit)
    def press(self,instance):
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

class MyApp(App):
    def build(self):
        #return Label(text="Hello World",font_size =72)
        return MyGridLayout()
if __name__ == '__main__':
    MyApp().run()