#kütüphanelerimiz ekledik
import os
from glob import glob
from numpy import array
from PIL import Image
import cv2
#verilerimizin klasörünü belirleyip kullanacağımız algoritmayı ve algılama modelini çağırıyoruz
path = "pic"
recognizer = cv2.face.LBPHFaceRecognizer.create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#verilerimizi ayrıştırmak için bir fonksiyon oluşturuyoruz
def getImagesAndLabels(path):
    imagePath = glob(path + '/*.jpg')
    faceSamples = []
    ids = []
    for index, imagePath in enumerate(imagePath):
        with Image.open(imagePath).convert('L') as PIL_img:
            img_numpy = array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        print(id)
        faces = detector.detectMultiScale(img_numpy)
        if len(faces) == 0:
            print(f"No faces found in {imagePath}")
            continue
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
    return faceSamples, ids
#verileri almak ve eğitmek
faces, ids = getImagesAndLabels('pic')
recognizer.train(faces, array(ids))
recognizer.write('code/code.yml')
