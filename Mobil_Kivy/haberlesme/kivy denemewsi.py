from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import requests
import cv2
import numpy as np
import threading

class VideoStreamApp(App):
    def build(self):
        self.img = Image()
        # Arka planda video verilerini çekmek için bir thread başlat
        threading.Thread(target=self.fetch_video_data, daemon=True).start()
        return self.img

    def fetch_video_data(self):
        """Video verilerini arka planda çeken fonksiyon."""
        try:
            with requests.get('http://192.168.0.103:5000/video_feed', stream=True, timeout=5) as response:
                content = b''
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # Daha büyük chunk boyutu
                    content += chunk
                    # Boundary'ye göre frame'leri ayır
                    start = content.find(b'\xff\xd8')
                    end = content.find(b'\xff\xd9')
                    if start != -1 and end != -1:
                        jpg = content[start:end + 2]
                        content = content[end + 2:]
                        nparr = np.frombuffer(jpg, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if frame is not None:
                            Clock.schedule_once(lambda dt: self.update_image(frame))
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
                self.img.texture = texture
            else:
                print("Received None frame")
        except Exception as e:
            print(f"Error updating image: {e}")


if __name__ == '__main__':
    VideoStreamApp().run()
