from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel


class MainApp(MDApp):
    def build(self):
        screen = MDScreen()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        label = MDLabel(
            text="Hello World",
            halign="center",
            valign="middle"
        )

        screen.add_widget(label)

        return screen


MainApp().run()
