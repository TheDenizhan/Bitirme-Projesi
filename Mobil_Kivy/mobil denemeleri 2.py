from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput


class LoginScreen(Screen):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = app

        layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text='Kullanıcı Adı')
        layout.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Şifre', password=True)
        layout.add_widget(self.password_input)
        login_button = Button(text='Giriş Yap')
        login_button.bind(on_press=self.login_pressed)
        layout.add_widget(login_button)
        self.status_label = Label(text='')
        layout.add_widget(self.status_label)
        self.add_widget(layout)

    def login_pressed(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username == "admin" and password == "admin":
            self.app.switch_to_main()
        else:
            self.status_label.text = 'Hatalı kullanıcı adı veya şifre'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Ana Ekran'))
        self.settings_button = Button(text='Ayarlar')
        self.settings_button.bind(on_press=self.switch_to_settings)
        layout.add_widget(self.settings_button)
        self.add_widget(layout)

    def on_enter(self, *args):
        self.settings_button.bind(on_press=self.switch_to_settings)

    def on_leave(self, *args):
        self.settings_button.unbind(on_press=self.switch_to_settings)

    def switch_to_settings(self, instance):
        self.manager.current = 'settings'


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Ayarlar Ekranı'))
        layout.add_widget(Button(text='Ana Ekrana Dön', on_press=self.switch_to_main))
        self.add_widget(layout)

    def switch_to_main(self, instance):
        self.manager.current = 'main'


class TheEyeApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        login_screen = LoginScreen(app=self, name='login')
        self.screen_manager.add_widget(login_screen)

        main_screen = MainScreen(name='main')
        self.screen_manager.add_widget(main_screen)

        settings_screen = SettingsScreen(name='settings')
        self.screen_manager.add_widget(settings_screen)

        return self.screen_manager

    def switch_to_main(self):
        self.screen_manager.current = 'main'

    def switch_to_settings(self):
        self.screen_manager.current = 'settings'


if __name__ == '__main__':
    TheEyeApp().run()
