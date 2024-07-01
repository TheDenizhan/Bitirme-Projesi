from flask import Flask, request, jsonify, Response
import cv2
import time
import threading
import tkinter as tk
from tkinter import Button

app = Flask(__name__)

# OpenCV video capture
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Lower resolution width
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Lower resolution height
# Function to take a picture
def take_picture():
    _, image = camera.read()
    cv2.imwrite('kapi.jpg', image)

# Function to take a video
def take_video():
    video_kayit = cv2.VideoWriter('kapivideo.mp4', cv2.VideoWriter.fourcc(*'H264'), 25.0, (640, 480))
    baslangic_zamani = time.time()
    kayit_suresi = 5  # saniye
    while True:
        ret, videoGoruntu = camera.read()
        video_kayit.write(videoGoruntu)
        if time.time() - baslangic_zamani > kayit_suresi:
            break
        if cv2.waitKey(50) & 0xFF == ord('x'):
            break

# Function to handle button click
def zil():
    print('Zil Çaldı')
    take_picture()  # Take a picture when the button is clicked

# Tkinter window creation
window = tk.Tk()
window.title("TheEye")
window.geometry("250x250")

# Create Button
zil_button = Button(window, text='Zil', command=zil, bg="red", fg="white", font=("Helvetica", 16))
zil_button.pack(pady=20)

# Flask routes
@app.route('/openthedoor', methods=['GET'])
def open_the_door():
    return 'Kapı Açıldı'

@app.route('/alarm', methods=['GET'])
def alarm():
    return 'Alarm Aktif'

@app.route('/take_picture', methods=['GET'])
def take_picture_route():
    take_picture()
    return "Fotoğraf başarıyla çekildi."

@app.route('/take_video', methods=['GET'])
def take_video_route():
    take_video()
    return "Video başarıyla kaydedildi."
@app.route('/video_feed', methods=['GET'])
def video_feed():
    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        audio_file.save('received_audio.wav')  # Sunucu tarafında dosyayı kaydet
        return "Ses dosyası alındı ve kaydedildi."
    return "Dosya bulunamadı", 400
if __name__ == '__main__':
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    flask_thread.start()

    # Start Tkinter main loop
    window.mainloop()
