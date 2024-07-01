from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.graphics.texture import Texture
import requests
import numpy as np
import cv2
import sounddevice as sd
import wave
import threading
from kivy.clock import Clock
from flask import Flask, request, jsonify
from kivymd.uix.bottomnavigation import MDBottomNavigation,MDBottomNavigationItem
from kivy.uix.image import Image
from kivymd.uix.list import OneLineListItem, OneLineAvatarListItem, ImageLeftWidget
from kivy.uix.popup import Popup
#Window.borderless = True  # Pencere çerçevesini gizle
Builder.load_string('''
#:import Factory kivy.factory.Factory
<FacePopups@Popup>:
    auto_dismiss: False
    title: 'Add Face'
    size_hint: 0.6, 0.4
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Nickname:'
        TextInput:
            id: nickname_input
            multiline: False
        Label:
            text: 'URL:'
        TextInput:
            id: url_input
            multiline: False
        BoxLayout:
            Button:
                text: 'Submit'
                on_release: app.root.submit_popup()
            Button:
                text: 'Cancel'
                on_release: root.dismiss()
<MyPopup@Popup>
    auto_dismiss:False
    title:'Are you sure you want to open the Door'
    size_hint:0.6,0.2
    pos: self.pos
    GridLayout:
        cols:2
        Button:
            text:'Yes'
            on_release:app.root.openD()
            on_release:root.dismiss()
        Button:
            text:'No'
            on_release:root.dismiss()

<MyBoxLayout>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "The Eye"
            pos_hint: {'x': 0, 'center_y': .5}
            left_action_items: [["menu", lambda x: None]]
            right_action_items: [["account-circle-outline", lambda x: None]]
       
        MDBottomNavigation:
            padding:0
            spacing:0
            
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
                        size_hint: (1,None)
                        height: 300              
                        Image:
                            id: video_image  # Fotoğrafın gösterileceği Image widget'ı
                            #size_hint: 1, 1
                            allow_stretch: True  # Resmin boyutlandırılmasına izin ver  
                    MDBoxLayout:        
                        size_hint: (1, None)
                        height: 300
                        pos_hint: {'x':0.03}
                        GridLayout:
                            cols: 2
                            #size_hint: (1, None)
                            height: 300
                            spacing: 5
                            padding: 10
                            
                            MDFillRoundFlatIconButton:
                                icon: "door-open"
                                icon_size:"40sp"
                                text:"Open Door "
                                font_size:"20"
                                #theme_icon_color: "Custom"
                                #icon_color: [0,0,0,1]
                                md_bg_color: [20/255, 166/255, 34/255, 1]
                                on_press : Factory.MyPopup().open()
                            MDFillRoundFlatIconButton:
                                icon: "camera"
                                text: "Take Photo"
                                font_size:"20"
                                icon_size:"40sp"
                                #icon_color: [0,0,0,1]
                                md_bg_color: [32/255, 96/255, 199/255, 1]
                                on_press : root.takePhoto()
                            MDFillRoundFlatIconButton:
                                icon: "microphone"
                                text: "   Speak      "
                                font_size:"20"
                                #icon_color: [0,0,0,1]
                                icon_size:"40sp"
                                md_bg_color: [212/255, 189/255, 78/255, 1]
                                on_press : root.on_press_record_and_send()
                                on_release: print("Konusma gonderildi")
                            MDFillRoundFlatIconButton:
                                icon: "bell"
                                icon_size:"40sp"
                                text: "  Alarm ! !   "
                                font_size:"20"
                                on_press : root.alarm()
                                #icon_color: [0,0,0,1]
                                md_bg_color: [199/255, 6/255, 64/255, 1]
                                
    
            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'List'
                icon: 'format-list-bulleted-square'
    
                ScrollView:
                    MDList:
                        id: video_list
                        
                    
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
                    on_release: Factory.FacePopups().open()
                    
            MDBottomNavigationItem:
                name: 'screen 4'
                text: 'Wifi-Settings'
                icon: 'wifi-settings'
    
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)
        
                    MDTextField:
                        id: server_ip_input
                        hint_text: "Enter Server IP"
                        helper_text: "This will update the server IP address"
                        helper_text_mode: "on_focus"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                        size_hint_x: None
                        width: 300
                        icon_right: "lan-connect"
                        icon_right_color: app.theme_cls.primary_color
        
                    MDRaisedButton:
                        text: "Save IP"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                        on_release: root.save_server_ip()
   
            
''')
server_ip = "127.0.0.1"  # Default IP, can be changed via GUI

class MyBoxLayout(FloatLayout):


    def save_server_ip(self):
        # Save the IP address from the TextInput to the variable
        server_ip = self.ids.server_ip_input.text
        print("Server IP updated to:", server_ip)
        # Optionally, you could save this IP to a file or settings for persistent storage
        return server_ip
    def submit_popup(self):
        print("Current ids:", self.ids)
        # Submit düğmesine basıldığında, girilen verileri al
        nickname = self.ids.nickname_input.text
        url = self.ids.url.text

        # Flask uygulamanızdaki ilgili endpoint'i çağır ve verileri ile
        endpoint = f'http://{server_ip}:5000/add_face'  # Uygun endpoint'i değiştirin
        data = {"nickname": nickname, "url": url}
        response = requests.post(endpoint, json=data)

        if response.status_code == 200:
            print("Veri başarıyla gönderildi.")
        else:
            print("Veri gönderilirken bir hata oluştu.")

        # Pop-up penceresini kapat
        self.dismiss()
    def record_audio(self, duration=5, sample_rate=44100):
        """Ses kaydını başlatır ve .wav dosyası olarak kaydeder."""
        print("Ses kaydı başlıyor...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
        sd.wait()  # Kaydın bitmesini bekle
        print("Ses kaydı tamamlandı.")

        # Kaydedilen sesi WAV dosyası olarak kaydet
        wav_file = 'recorded_audio.wav'
        wf = wave.open(wav_file, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(np.array(recording, dtype=np.int16))
        wf.close()
        return wav_file

    def send_audio_to_server(self, audio_file):
        """Ses dosyasını sunucuya gönderir."""
        url = f'http://{server_ip}:5000/upload_audio'
        files = {'audio': open(audio_file, 'rb')}
        response = requests.post(url, files=files)
        print(f"Ses dosyası gönderildi: {response.text}")

    def on_press_record_and_send(self):
        """Butona basıldığında ses kaydını başlatır ve sunucuya gönderir."""
        audio_file = self.record_audio()
        self.send_audio_to_server(audio_file)
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
        response = requests.get(f'http://{server_ip}:5000/take_picture')
        if response.status_code == 200:
            print("Bilgisayara fotoğraf çekme sinyali gönderildi.")
            photo_url = 'D:\Self_Devoloping\Projeler\Bitirme_Projesi\Mobil_Kivy\kapi.jpg'

            # Fotoğrafı göster
            self.show_photo(photo_url)
        else:
            print("Hata: Sinyal gönderilemedi.")

        print(response.status_code)
    def openD(self):
        response = requests.get(f'http://{server_ip}:5000/openthedoor')
        if response.status_code == 200:
           data = response.text
           print(f'The Door is {data}')
        else:
            print("Hata:")

    def show_photo(self, photo_url):
        # Fotoğrafı göstermek için URL'yi kullanarak Image widget'ını güncelle
        self.ids.photo.source = photo_url

    def alarm(self):
        response = requests.get(f'http://{server_ip}:5000/alarm')
        if response.status_code == 200:
            data = response.text
            print(f'{data} is ON')
        else:
            print("Hata:")

    def fetch_video_list(self):
        """Sunucudan video listesini çeker ve list widget'ını günceller."""
        try:
            response = requests.get(f'http://{server_ip}:5000/get_videos')
            video_files = response.json()  # JSON yanıtını Python listesine çevir
            self.ids.video_list.clear_widgets()
            for video in video_files:
                video_path = video['video_path']
                list_item = OneLineListItem(text=video_path, on_press=lambda x, vp=video_path: self.play_video(vp))
                self.ids.video_list.add_widget(list_item)
        except requests.RequestException as e:
            print(f"Sunucuyla bağlantı hatası: {e}")

    def play_video(self, video_file):
        # Video dosyasını çalmak için bir fonksiyon
        print(f"Playing video: {video_file}")

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
        layout.fetch_video_list()  # Listeyi çek ve oluştur
        layout.fetch_faces_list()  # Yüz listesini çek ve oluştur
        # Arka planda video verilerini çekmek için bir thread başlat
        threading.Thread(target=layout.fetch_video_data, daemon=True).start()
        #Clock.schedule_interval(layout.update_image, 1.0 / 1500)  # Her 30 milisaniyede bir görüntüyü güncelle
        return layout


app = Flask(__name__)
if __name__ == "__main__":

    MainApp().run()
