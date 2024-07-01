import pyaudio
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.graphics.texture import Texture
import requests
import numpy as np
from kivy.uix.gridlayout import GridLayout
import cv2
import time
from kivy.uix.button import Button
import simpleaudio as sa
import io
import sounddevice as sd
import wave
import threading
from kivy.clock import Clock
from flask import Flask, request, jsonify
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.image import Image
from kivymd.uix.list import OneLineListItem, OneLineAvatarListItem, ImageLeftWidget,ImageLeftWidgetWithoutTouch
from kivy.uix.popup import Popup

# Window.borderless = True  # Pencere çerçevesini gizle
Builder.load_string('''
#:import Factory kivy.factory.Factory

<MyPopup@Popup>:
    auto_dismiss: False
    title: 'Are you sure you want to open the Door'
    size_hint: 0.6, 0.2
    pos: self.pos
    GridLayout:
        cols: 2
        Button:
            text: 'Yes'
            on_release: app.root.openD()
            on_release: root.dismiss()
        Button:
            text: 'No'
            on_release: root.dismiss()

<MyBoxLayout>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "The Eye"
            pos_hint: {'x': 0, 'center_y': .5}
            right_action_items: [['account-circle-outline', lambda x: app.root.ask_for_login()]]

        ScreenManager:
            id: screen_manager
            Screen:
                name: 'login'
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            
                    Image:
                        source: 'D:/Self_Devoloping/Projeler/Bitirme_Projesi/TheEye_MobilApp/Uygulama/TheEye.jpg'
                        size_hint: .4,.4
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            
                    MDTextField:
                        id: email_input
                        hint_text: "Email"
                        size_hint_x: None
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        width: "300dp"
                        mode: "fill"
            
                    MDTextField:
                        id: password_input
                        hint_text: "Password"
                        size_hint_x: None
                        width: "300dp"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                        mode: "fill"
                        password: True
            
                    MDRaisedButton:
                        text: "Login"
                        size_hint_x: None
                        width: "300dp"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        on_release: app.root.login(email_input.text, password_input.text)

            Screen:
                name: 'home'
                MDBottomNavigation:
                    padding: 0
                    spacing: 0

                    MDBottomNavigationItem:
                        name: 'screen 1'
                        text: 'Home'
                        icon: 'home'
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint: (None, None)
                            size: (450, 600)  # Image ve buttons grid'in toplam yüksekliği
                            pos_hint: {'center_x': 0.5, 'center_y': 0.4}

                            MDBoxLayout:
                                size_hint: (1, None)
                                height: 300
                                Image:
                                    id: video_image  # Fotoğrafın gösterileceği Image widget'ı
                                    allow_stretch: True  # Resmin boyutlandırılmasına izin ver
                            MDBoxLayout:
                                size_hint: (1, None)
                                height: 300
                                pos_hint: {'x': 0.03}
                                GridLayout:
                                    cols: 2
                                    height: 300
                                    spacing: 5
                                    padding: 10

                                    MDFillRoundFlatIconButton:
                                        icon: "door-open"
                                        icon_size: "40sp"
                                        text: "Open Door "
                                        font_size: "20"
                                        md_bg_color: [20/255, 166/255, 34/255, 1]
                                        on_press: Factory.MyPopup().open()
                                    MDFillRoundFlatIconButton:
                                        icon: "camera"
                                        text: "Take Photo"
                                        font_size: "20"
                                        icon_size: "40sp"
                                        md_bg_color: [32/255, 96/255, 199/255, 1]
                                        on_press: root.takePhoto()
                                    MDFillRoundFlatIconButton:
                                        icon: "microphone"
                                        text: "   Speak      "
                                        font_size: "20"
                                        icon_size: "40sp"
                                        md_bg_color: [212/255, 189/255, 78/255, 1]
                                        on_press: root.send_audio()
                                        on_release: print("Konusma gonderildi")
                                    MDFillRoundFlatIconButton:
                                        icon: "bell"
                                        icon_size: "40sp"
                                        text: "  Alarm ! !   "
                                        font_size: "20"
                                        on_press: root.alarm()
                                        md_bg_color: [199/255, 6/255, 64/255, 1]

                    MDBottomNavigationItem:
                        name: 'screen 2'
                        text: 'List'
                        icon: 'format-list-bulleted-square'

                        ScrollView:
                            MDList:
                                id: photos_list
                                padding: dp(10)

                    MDBottomNavigationItem:
                        name: 'screen 3'
                        text: 'Accounts'
                        icon: 'account-supervisor-outline'

                        ScrollView:
                            MDList:
                                id: faces_list
                                padding: dp(10)

                        MDFloatingActionButton:
                            icon: "plus"
                            pos_hint: {"right": .98, "y": .01}
                            on_release: app.root.show_url_nickname_popup()

''')
server_ip = "127.0.0.1"  # Default IP, can be changed via GUI
OUTPUT_FILENAME = 'client_output.wav'
RECORD_SECONDS = 5
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100



class MyBoxLayout(FloatLayout):
    def ask_for_login(self):
        self.ids.screen_manager.current = "login"

    def login(self, email, password):
        # E-posta ve şifreyi al
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        # Sunucuya gönderilecek veri
        data = {'email': email, 'password': password}

        # Sunucu URL'si
        server_url = f'http://{server_ip}:5000/login'

        # POST isteği gönder
        response = requests.post(server_url, json=data)

        # Yanıt kontrolü
        if response.status_code == 200:
            print("Başarıyla giriş yapıldı.")
            # Giriş başarılıysa ana ekran görünümüne geç
            self.ids.screen_manager.current = "home"
        else:
            print("Giriş başarısız. Lütfen tekrar deneyin.")
    def save_server_ip(self):
        # Save the IP address from the TextInput to the variable
        server_ip = self.ids.server_ip_input.text
        print("Server IP updated to:", server_ip)
        # Optionally, you could save this IP to a file or settings for persistent storage
        return server_ip

    def show_url_nickname_popup(self):
        # URL girişi için TextInput
        url_input = TextInput(hint_text="Enter URL", multiline=False,size_hint=(0.2, 0.05))

        # Nickname girişi için TextInput
        nickname_input = TextInput(hint_text="Enter Nickname", multiline=False,size_hint=(0.2, 0.05))

        # Kaydetme düğmesi oluştur
        save_button = Button(text='Save', size_hint=(0.2, 0.1), background_color=(214/255, 62/255, 19/255, 1), background_normal='')
        close_button = Button(text='Close', size_hint=(0.2, 0.1), background_color=(214/255, 62/255, 19/255, 1), background_normal='')
        # İçerik düzenini oluştur
        content_layout = GridLayout(cols=1, padding=10, spacing=10)
        content_layout.add_widget(url_input)
        content_layout.add_widget(nickname_input)
        content_layout.add_widget(save_button)
        content_layout.add_widget(close_button)

        # Popup oluştur ve düzeni ayarla
        popup = Popup(title='URL and Nickname',
                      content=content_layout,
                      size_hint=(.8, .7),

                      background_color=[214/255, 62/255, 19/255,  0.5]
                      )

        # Save button'a basıldığında yapılacak işlem
        def save_inputs(instance):
            url = url_input.text
            nickname = nickname_input.text
            print("URL:", url)
            print("Nickname:", nickname)
            # Sunucuya POST isteği yaparak add_face fonksiyonunu çağır
            server_url = f'http://{server_ip}:5000/add_face'  # Sunucu adresi ve istek yapılacak yol
            data = {'nickname': nickname, 'url': url}  # Gönderilecek veri
            response = requests.post(server_url, json=data)  # POST isteği yap

            if response.status_code == 200:
                print("Yeni yüz başarıyla eklendi.")
            else:
                print("Yüz eklenirken bir hata oluştu.")
            self.fetch_faces_list()
            popup.dismiss()

        save_button.bind(on_press=save_inputs)  # Save button'a basıldığında save_inputs fonksiyonunu çağır
        close_button.bind(on_press=popup.dismiss) # Close button
        content_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # İçerik düzenini popup'ın ortasına yerleştir
        popup.open()


    def record_audio(self,output_filename):
        """Record audio using PyAudio."""
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio to a wave file
        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    def send_audio(self):
        """Record and send audio to the server via HTTP POST."""
        self.record_audio(OUTPUT_FILENAME)
        url = f'http://{server_ip}:5000/upload_audio'
        files = {'audio': open(OUTPUT_FILENAME, 'rb')}
        response = requests.post(url, files=files)
        print(f"Ses dosyası gönderildi: {response.text}")
    def fetch_and_play_audio(self):
        """Fetch audio from the server and play it."""
        try:
            response = requests.get(f'http://{server_ip}:5000/send_audio', stream=True)
            print('bu bir response mesajıdır',response)
            if response.status_code == 200:
                # Load the audio content into BytesIO
                audio_data = io.BytesIO(response.content)
                audio_data.seek(0)  # Go to the beginning of the BytesIO stream

                # Play the audio file
                wave_obj = sa.WaveObject.from_wave_file(audio_data)
                play_obj = wave_obj.play()
                play_obj.wait_done()

                print("Audio played successfully.")
            else:
                print("Failed to download audio from server:", response.status_code)
        except Exception as e:
            print("An error occurred while downloading or playing audio:", str(e))
    def continuously_check_audio(self):
        """Continuously check for new audio from the server."""
        while True:
            self.fetch_and_play_audio()
            # Wait for a certain amount of time before checking again
    def fetch_video_data(self):
        """Video verilerini arka planda çeken fonksiyon."""
        try:
            with requests.get(f'http://{server_ip}:5000/video_feed', stream=True, timeout=5) as response:
                content = b''
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # Daha büyük chunk boyutu
                    content += chunk
                    start = content.find(b'\xff\xd8')  # JPEG start
                    end = content.find(b'\xff\xd9', start)  # JPEG end
                    if start != -1 and end != -1:
                        jpg = content[start:end + 2]
                        content = content[end + 2:]
                        nparr = np.frombuffer(jpg, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if frame is not None:
                            # Görüntüyü 180 derece döndür
                            frame = cv2.flip(frame, -1)
                            Clock.schedule_once(lambda dt, frm=frame: self.update_image(frm))
                        else:
                            print("Invalid frame received")
                    else:
                        print("Incomplete frame data, continuing...")
        except requests.RequestException as e:
            print(f"Network error: {e}")
        except Exception as e:
            print(f"Error during video fetching or decoding: {e}")
    def update_image(self, frame, *args):
        """UI thread'inde Image widget'ını güncelleyen fonksiyon."""
        try:
            if frame is not None:
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')
                self.ids.video_image.texture = texture
            else:
                print("Received None frame")
        except Exception as e:
            print(f"Error updating image: {e}")
    def takePhoto(self):
        response = requests.get(f'http://{server_ip}:5000/pic')
        self.fetch_photos_list()
        #buraya veri tabanına kaydedilecek yolu eklemesini yaz
    def openD(self):
        response = requests.get(f'http://{server_ip}:5000/openthedoor')
        if response.status_code == 200:
            data = response.text
            print(f'The Door is {data}')
        else:
            print("Hata:")
    def alarm(self):
        response = requests.get(f'http://{server_ip}:5000/alarm')
        if response.status_code == 200:
            data = response.text
            print(f'{data} is ON')
        else:
            print("Hata:")
    def fetch_photos_list(self):
        """Sunucudan yüz listesini çeker ve list widget'ını günceller."""
        try:
            response = requests.get(f'http://{server_ip}:5000/get_photos')
            photos = response.json()  # JSON yanıtını Python listesine çevir
            self.ids.photos_list.clear_widgets()
            for photo in photos:
                photo_path = photo['photo_path']
                list_item = OneLineAvatarListItem(text=photo_path)
                image_widget = ImageLeftWidget(source=photo_path)  # Avatar resmi
                list_item.add_widget(image_widget)

                # Eklenen her öğe için on_press davranışını tanımla
                list_item.bind(on_press=lambda instance, url=photo_path: self.show_photo_popup(url))

                self.ids.photos_list.add_widget(list_item)
        except requests.RequestException as e:
            print(f"Sunucuyla bağlantı hatası: {e}")
    def show_photo_popup(self, photo_url):
        # Fotoğrafın gösterileceği bir Image widget'ı oluştur
        image = Image(source=photo_url, size_hint=(.9, .8))

        # Kapatma düğmesi oluştur
        close_button = Button(text='Close', size_hint=(.2, .1),background_color=[214/255, 62/255, 19/255, 1],background_normal="")
        close_button.bind(on_press=lambda instance: popup.dismiss())  # Popup'ı kapatmak için on_press davranışı

        # İçerik düzenini oluştur
        content_layout = GridLayout(cols=1, padding=10, spacing=10)
        content_layout.add_widget(image)
        content_layout.add_widget(close_button)

        # Popup oluştur ve düzeni ayarla
        popup = Popup(title='Photo',
                      content=content_layout,
                      size_hint=(.8, .7),
                      background_color=[1, 0.6, 0.4, 0.5]
                      )

        # Assign IDs to the widgets
        self.ids.popup_image = image
        self.ids.popup_close_button = close_button

        content_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # İçerik düzenini popup'ın ortasına yerleştir
        popup.open()
    def fetch_faces_list(self):
        """Sunucudan yüz listesini çeker ve list widget'ını günceller."""
        try:
            response = requests.get(f'http://{server_ip}:5000/get_faces')
            faces = response.json()  # JSON yanıtını Python listesine çevir
            self.ids.faces_list.clear_widgets()
            for face in faces:
                avatar_path = face['img_path']
                nickname = face['nickname']
                list_item = OneLineAvatarListItem(text=nickname)
                image_widget = ImageLeftWidget(source=avatar_path)  # Avatar resmi
                list_item.add_widget(image_widget)
                self.ids.faces_list.add_widget(list_item)
        except requests.RequestException as e:
            print(f"Sunucuyla bağlantı hatası: {e}")


class MainApp(MDApp):

    def build(self):
        # Temanın özel renklerini ayarlamak için MDApp sınıfının başlatıcı metodunda kullanın
        self.theme_cls.theme_style = "Light"  # Temayı aydınlık (Light) olarak ayarla
        self.theme_cls.primary_palette = "DeepOrange"  # Tema paletini ayarla
        layout = MyBoxLayout()
        self.img = Image()
        layout.fetch_photos_list()  # Listeyi çek ve oluştur
        layout.fetch_faces_list()  # Yüz listesini çek ve oluştur
        # Arka planda video verilerini çekmek için bir thread başlat
        threading.Thread(target=layout.fetch_video_data, daemon=True).start()
        # Start the continuous audio check in a background thread
        threading.Thread(target=layout.continuously_check_audio, daemon=True).start()

        # Clock.schedule_interval(layout.update_image, 1.0 / 1500)  # Her 30 milisaniyede bir görüntüyü güncelle
        return layout


app = Flask(__name__)
if __name__ == "__main__":
    MainApp().run()
