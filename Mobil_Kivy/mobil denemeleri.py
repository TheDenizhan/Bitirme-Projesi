from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.video import Video
import requests
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window
class TheEyeApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        take_pic_button = Button(text='Fotoğraf Çek', on_press=self.take_pic)
        self.layout.add_widget(take_pic_button)

        take_vid_button = Button(text='Video Çek', on_press=self.take_vid)
        self.layout.add_widget(take_vid_button)

        self.photo = Image()  # Fotoğrafın gösterileceği Image widget'ı
        self.layout.add_widget(self.photo)

        player = VideoPlayer(
            source="kapivideo.mp4",
            size_hint=(0.8, 0.8),
            options={'fit_mode': 'contain'}
        )
        player.state = 'play'
        player.options = {'eos': 'loop'}
        player.allow_stretch = True
        self.layout.add_widget(player)
        return self.layout

    def take_pic(self, instance):
        # Bilgisayara sinyal gönder
        response = requests.get('Http://192.168.0.103:5000/take_picture')
        if response.status_code == 200:
            print("Bilgisayara fotoğraf çekme sinyali gönderildi.")
            photo_url = 'kapi.jpg'

            # Fotoğrafı göster
            self.show_photo(photo_url)
        else:
            print("Hata: Sinyal gönderilemedi.")

    def take_vid(self, instance):
        # Bilgisayara sinyal gönder
        response = requests.get('http://192.168.0.103:5000/take_video')

        if response.status_code == 200:
            print("Bilgisayara video çekme sinyali gönderildi.")

        else:
            print("Hata: Sinyal gönderilemedi.")

    def update_video(self, video_url):
        self.video.source = video_url
        self.video.state = 'play'

    def show_photo(self, photo_url):
        # Fotoğrafı göstermek için URL'yi kullanarak Image widget'ını güncelle
        self.photo.source = photo_url

if __name__ == '__main__':
    TheEyeApp().run()
