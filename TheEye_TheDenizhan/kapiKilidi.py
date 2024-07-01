
import time
import requests
import cv2

#Ardunio bağlantısı için Serial kütüphanesini kullanacağız
import serial

import tkinter as tk
from tkinter import Button
#haberleşeceğimiz portumuzu com4 olarak ayarlayarak baudrate'i ardunioyu kodladığımız baudrate ile aynı ayarlıyoruz.
#haberleşme süresini 0.10 olarak ayarlayıp ardunio değişkenine atıyoruz.
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
def sorgu():
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    recognizer.read('code/code.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    cam2 = cv2.VideoCapture(0)
    while True:
        ret, img2 = cam2.read()
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 15)
        for (x, y, w, h) in faces:
            cv2.rectangle(img2, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 4)
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if 0 < Id < 32 and confidence < 70:
                Id = "hasan"
                return Id
            elif 32 < Id < 63 and confidence < 70:
                Id = "hamza"
                return Id
            else:
                Id = "else"
                return Id


def take_pic():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('kapi.jpg', image)


def take_vid():
    kamera = cv2.VideoCapture(0)
    video_kayit = cv2.VideoWriter('kapivideo.avi', cv2.VideoWriter.fourcc(*'XVID'), 25.0, (640, 480))
    baslangic_zamani = time.time()
    kayit_suresi = 5  # saniye
    while True:
        ret, videoGoruntu = kamera.read()
        video_kayit.write(videoGoruntu)
        if time.time() - baslangic_zamani > kayit_suresi:
            break
        if cv2.waitKey(50) & 0xFF == ord('x'):
            break


def access_approved():
    arduino.write(b'3')


def access_denied():
    arduino.write(b'1')


def zil():
    arduino.write(b'2')
    rec = sorgu()
    if rec == 'else':
        take_pic()
        access_denied()
        send_telegram_message()
    else:
        access_approved()


def send_telegram_message():
    telegram_url = f'https://api.telegram.org/bot6835603068:AAFYzX0veRpNagQuYGCWDigrw_DO52ltpMA/sendMessage'
    message_text = 'Kapida biri var.'

    # Replace with your Telegram chat ID
    params = {
        'chat_id': 1363718509,
        'text': message_text,
    }

    response = requests.post(telegram_url, params=params)
    print(response.text)


def create_button(window):
    zil_button = Button(window, text='Zil', command=zil, bg="red", fg="white", font=("Helvetica", 75))
    zil_button.pack(pady=20)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("TheEye")
    window.geometry("250x250")
    create_button(window)
    window.mainloop()
