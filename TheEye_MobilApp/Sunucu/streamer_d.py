import os
import wave

import serial
import simpleaudio as sa
import pyaudio
from flask import Flask, request, jsonify, Response,send_file
import cv2
import time
import threading
import tkinter as tk
from tkinter import Button
import sqlite3
import random
import string
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)
app = Flask(__name__)

# Setup face recognition
recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read('code/code.yml')
cascade_path = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
def init_db():
    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        # access_persons tablosunu oluşturma
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password TEXT,
                token TEXT
            )
        ''')

        # faces tablosunu oluşturma
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT,
                img_path TEXT
            )
        ''')

        # videos tablosunu oluşturma
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_path TEXT
            )
        ''')

        conn.commit()


def add_sample_person():
    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        name = "admin"
        surname = "admin"
        email = "admin@example.com"
        phone = "1234567890"
        password = "admin"
        token = generate_random_token(10)

        cursor.execute('''
            INSERT INTO access_persons (name, surname, email, phone, password, token)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, surname, email, phone, password, token))

        conn.commit()
@app.route('/login', methods=['POST'])
def login():
    # İstekten gelen JSON verilerini al
    request_data = request.json
    email = request_data.get('email')
    password = request_data.get('password')

    # E-posta ve şifreyi kontrol etmek için veritabanını sorgula
    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        # E-posta ve şifreyi içeren kullanıcıyı sorgula
        cursor.execute("SELECT * FROM access_persons WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            # Kullanıcı bulundu, başarılı giriş mesajı gönder
            return jsonify({'success': 'Login successful'}), 200
        else:
            # Kullanıcı bulunamadı, hata mesajı gönder
            return jsonify({'error': 'Invalid email or password'}), 401

def generate_random_token(length=10):
    # Belirtilen uzunlukta rastgele bir token oluşturur
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))
# OpenCV video capture


@app.route('/get_photos', methods=['GET'])
def get_photos():
    with sqlite3.connect('application.db') as conn:
        conn.row_factory = sqlite3.Row  # Row objeleri olarak sonuçları almak için
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM photos")
        photos = cursor.fetchall()
        photo_list = [dict(photo) for photo in photos]  # Rowları dictionary'e çevir
    return jsonify(photo_list)
@app.route('/pic', methods=['GET'])
def take_picture():
    _, image = camera.read()
    i = 0
    while os.path.exists(f'D:\Self_Devoloping\Projeler\Bitirme_Projesi\TheEye_MobilApp\Sunucu\pictures\pic_{i}.jpg'):
        i += 1
    path = f'D:\Self_Devoloping\Projeler\Bitirme_Projesi\TheEye_MobilApp\Sunucu\pictures\pic_{i}.jpg'

    cv2.imwrite(path, image)
    add_sample_photos(path)
    return f'Picture saved as {path}'
def add_sample_photos(path):

    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        #Scursor.execute("DELETE FROM photos")
        cursor.execute("INSERT INTO photos (photo_path) VALUES (?)", (path,))
        conn.commit()





def take_video():
    video_kayit = cv2.VideoWriter('kapivideo.mp4', cv2.VideoWriter.fourcc(*'H264'), 25.0, (640, 480))
    baslangic_zamani = time.time()
    kayit_suresi = 5
    while True:
        ret, videoGoruntu = camera.read()
        video_kayit.write(videoGoruntu)
        if time.time() - baslangic_zamani > kayit_suresi:
            break
        if cv2.waitKey(50) & 0xFF == ord('x'):
            break

def zil():
    print('Zil Çaldı')
    arduino.write(b'2')

# Recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = 'server_output.wav'
Message_FILENAME = 'Server_Message.wav'
@app.route('/send_audio', methods=['GET'])
def send_audio():
    """Endpoint to send the recorded audio file to the client."""
    try:
        # Ensure the audio is re-recorded before sending
        record_audio(OUTPUT_FILENAME)

        # Check if the file exists before sending
        if not os.path.exists(OUTPUT_FILENAME):
            raise FileNotFoundError(f"File {OUTPUT_FILENAME} does not exist.")

        # Send the file to the client
        return send_file(OUTPUT_FILENAME, mimetype='audio/wav', as_attachment=True)

    except FileNotFoundError as fnfe:
        print(f"File not found error: {str(fnfe)}")
        return jsonify({"error": "Audio file not found."}), 404

    except Exception as e:
        print(f"Error while sending audio: {str(e)}")
        return jsonify({"error": str(e)}), 500

def record_audio(output_filename):
    """Record audio for the specified number of seconds."""
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        print("Recording...")
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    except Exception as e:
        print(f"Error while recording audio: {str(e)}")

def record_audio2():
    record_audio(Message_FILENAME)
def play_audio2():
    play_audio(Message_FILENAME)
def sorgu():

        success, frame = camera.read()



        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 15)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 4)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if 0 < Id < 151 and confidence < 80:

                arduino.write(b'3')

            else:
                arduino.write(b'1')


window = tk.Tk()
window.title("TheEye")
window.geometry("500x500")

# Butonları oluşturma ve yerleştirme
zil_button = tk.Button(window, text='Zil', command=zil, bg="red", fg="white", font=("Helvetica", 46))
zil_button.grid(row=0, column=0, sticky="nsew")

record_button1 = tk.Button(window, text="Mesaj Bırak", command=record_audio2, bg="red", fg="white", font=("Helvetica", 46))
record_button1.grid(row=0, column=1, sticky="nsew")

record_button2 = tk.Button(window, text="Kapı Aç", command=sorgu, bg="red", fg="white", font=("Helvetica", 46))
record_button2.grid(row=1, column=0, sticky="nsew")

record_button3 = tk.Button(window, text="Mesajı Dinle", command=play_audio2, bg="red", fg="white", font=("Helvetica", 46))
record_button3.grid(row=1, column=1, sticky="nsew")

# Grid içindeki hücrelerin boyutlarını eşit şekilde ayarlama
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)



@app.route('/openthedoor', methods=['GET'])
def open_the_door():
    arduino.write(b'3')
    return 'Kapı Açıldı'

@app.route('/alarm', methods=['GET'])
def alarm():
    arduino.write(b'4')
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

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 15)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 4)
                    Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                    if 0 < Id < 151 and confidence < 80:
                        Id = "Hasan"


                    else:
                        Id = "Stranger"


                    # Yüz etiketini görüntü üzerine yaz
                    cv2.putText(frame, str(Id), (x - 20, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/add_face', methods=['POST'])
def add_face():
    # POST isteğinden nickname ve img_url parametrelerini al
    nickname = request.json.get('nickname')
    img_url = request.json.get('url')

    if not nickname or not img_url:
        return jsonify({'error': 'Lütfen geçerli bir nickname ve img_url sağlayın.'}), 400

    # Veritabanına yüz eklemek için gerekli işlemleri yap
    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        #cursor.execute("DELETE FROM faces")
        cursor.execute("INSERT INTO faces (nickname, img_path) VALUES (?, ?)", (nickname, img_url))
        conn.commit()

    return jsonify({'success': 'Yeni yüz başarıyla eklendi.'}), 200
def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        saved_sound = 'received_audio.wav'
        audio_file.save(saved_sound)
        play_audio(saved_sound)
        return "Ses dosyası alındı ve kaydedildi."
    return "Dosya bulunamadı", 400
@app.route('/get_faces', methods=['GET'])
def get_faces():
    """Veritabanından yüz listesini alır ve JSON formatında döner."""
    with sqlite3.connect('application.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faces")
        faces = cursor.fetchall()
        face_list = [dict(face) for face in faces]
    return jsonify(face_list)
# Basit bir rota tanımlayın
@app.route('/')
def home():
    return "Merhaba, Flask Sunucusuna Hoşgeldiniz!"
def run_flask_app():
    # Flask uygulamasını başlatma işlemi
    app.run(host='0.0.0.0',port=5000)
if __name__ == '__main__':
    init_db()  # Veritabanını başlat
    print("Token:", generate_random_token(20))  # 20 karakterlik rastgele bir token üret


    # Flask uygulamasını ayrı bir thread'de başlat
    flask_thread = threading.Thread(target=run_flask_app)

    flask_thread.start()
    window.mainloop()
