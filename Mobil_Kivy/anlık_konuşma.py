from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
import cv2
from threading import Thread

class VideoThread(Thread):
    def __init__(self, app):
        super(VideoThread, self).__init__()
        self.app = app
        self.stop_event = False

    def run(self):
        cap = cv2.VideoCapture(0)
        while not self.stop_event:
            ret, frame = cap.read()
            if ret:
                self.app.update_video(frame)

    def stop(self):
        self.stop_event = True

class TheEyeApp(App):
    def __init__(self, **kwargs):
        super(TheEyeApp, self).__init__(**kwargs)
        self.video_thread = None

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.video = Video(source='', state='play')
        self.layout.add_widget(self.video)

        return self.layout

    def on_start(self):
        self.video_thread = VideoThread(self)
        self.video_thread.start()

    def on_stop(self):
        if self.video_thread:
            self.video_thread.stop()

    def update_video(self, frame):
        # OpenCV kareyi Kivy uyumlu hale getir
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_texture = frame.tobytes()
        self.video.texture = frame_texture

if __name__ == '__main__':
    TheEyeApp().run()
