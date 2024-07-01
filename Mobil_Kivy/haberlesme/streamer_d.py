from flask import Flask, request, jsonify, Response
import cv2
import time
import threading
import tkinter as tk
from tkinter import Button
import sqlite3
import random
import string
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
def generate_random_token(length=10):
    # Belirtilen uzunlukta rastgele bir token oluşturur
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))
# OpenCV video capture


@app.route('/get_videos', methods=['GET'])
def get_videos():
    """Veritabanından video listesini alır ve JSON formatında döner."""
    with sqlite3.connect('application.db') as conn:
        conn.row_factory = sqlite3.Row  # Row objeleri olarak sonuçları almak için
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()
        video_list = [dict(video) for video in videos]  # Rowları dictionary'e çevir
    return jsonify(video_list)

def take_picture():
    _, image = camera.read()
    cv2.imwrite('kapi.jpg', image)

def add_sample_videos():
    video_paths = [
        'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/videos/video_1.mp4',
        'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/videos/video_2.mp4',
        'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/videos/video_3.mp4'

    ]
    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM videos")  # Mevcut kayıtları temizle
        for path in video_paths:
            cursor.execute("INSERT INTO videos (video_path) VALUES (?)", (path,))
        conn.commit()
def add_sample_faces():
    faces_data = [
        ('Ahmet Savli', 'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/faces/ahmet.jpg'),
        ('Fatma Pamuk', 'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/faces/fatma.jpg'),
        ('Hasan Denizhan', 'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/faces/hasan.jpg'),
        ('Lee Sin', 'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/faces/lee.jpg'),
        ('Zeynep Savli', 'D:/Self_Devoloping/Projeler/Bitirme_Projesi/Mobil_Kivy/faces/zeynep.jpg')
    ]
    with sqlite3.connect('application.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM faces")  # Önceden var olan kayıtları temizle
        for nickname, img_path in faces_data:
            cursor.execute("INSERT INTO faces (nickname, img_path) VALUES (?, ?)", (nickname, img_path))
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
    take_picture()

window = tk.Tk()
window.title("TheEye")
window.geometry("250x250")
zil_button = Button(window, text='Zil', command=zil, bg="red", fg="white", font=("Helvetica", 16))
zil_button.pack(pady=20)

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

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 15)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 4)
                    Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                    if 0 < Id < 51 and confidence < 80:
                        Id = "Hasan"
                        print(Id, confidence)

                    else:
                        Id = "Stranger"
                        print(Id, confidence)
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
        cursor.execute("INSERT INTO faces (nickname, img_path) VALUES (?, ?)", (nickname, img_url))
        conn.commit()

    return jsonify({'success': 'Yeni yüz başarıyla eklendi.'}), 200
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        audio_file.save('received_audio.wav')
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
    add_sample_faces()
    add_sample_videos()
    # Flask uygulamasını ayrı bir thread'de başlat
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    window.mainloop()
