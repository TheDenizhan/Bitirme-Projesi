from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

kv = '''
MDBoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: "AppBar small"
        type: "top"
        elevation: 10
        left_action_items: [["menu", lambda x: None]]
        right_action_items: [["account-circle-outline", lambda x: None]]

MDScreen:
    md_bg_color: app.theme_cls.secondary_dark

    MDLabel:
        text: "Hello World"
        halign: "center"
        valign: "middle"
'''

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"  # "Purple", "Red"
        return Builder.load_string(kv)

MainApp().run()