from flask import Flask, request, jsonify
import cv2
import time
import serial
import threading
import tkinter as tk
from tkinter import Button
app = Flask(__name__)
#arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)

@app.route('/openthedoor', methods=['GET'])
def open_the_door():
    #arduino.write(b'3')

    return 'opened'
@app.route('/alarm', methods=['GET'])
def alarm():
    #arduino.write(b'3')

    return 'alarm'

@app.route('/take_picture', methods=['GET'])
def take_picture():
    camera = cv2.VideoCapture(0)
    _, image = camera.read()
    cv2.imwrite('kapi.jpg', image)
    camera.release()

    return "Fotoğraf başarıyla çekildi."

@app.route('/take_video', methods=['GET'])
def take_video():
    camera = cv2.VideoCapture(0)
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

    return "Video başarıyla kaydedildi."

def create_button(window):
    zil_button = Button(window, text='Zil', command=zil, bg="red", fg="white", font=("Helvetica", 75))
    zil_button.pack(pady=20)

def access_approved():
    #arduino.write(b'3')
    print('Access approved')


def access_denied():
    #arduino.write(b'1')
    print('Access denied')

def zil():
    print('zil caldi')
    #arduino.write(b'2')
    #rec = sorgu()
    #if rec == 'else':
    #    take_pic()
     #   access_denied()
     #   send_telegram_message()
    #else:
    #    access_approved()

if __name__ == '__main__':
    # Create Tkinter window
    window = tk.Tk()
    window.title("TheEye")
    window.geometry("250x250")
    create_button(window)

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    flask_thread.start()

    # Start Tkinter main loop
    window.mainloop()
