#OpenCV kütüphanemizi ekliyoruz
import cv2
#Bilgisayarımızın kamerasından alınan görüntüyü değişkene atıyoruz
vid_cam = cv2.VideoCapture("Video_Kayit.mp4")
#yüz algılama modelimizi yüklüyoruz
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#verilerimizi kaydederken tanımlayacağımız değişkenleri oluşturuyoruz
face_id = 0
count = 0
count2=count+50
member_name = "DenizhanHasan"
#birden fazla fotoğraf çekeceğimiz için bir döngü oluşturuyoruz
while (True):
    #kameradan aldığımız görüntülerimizi okuyoruz ve gri tonlama uyguluyoruz
    _, img_frame = vid_cam.read()
    gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
    #algıladığımız yüz için fotoğraf çekmesini isticeğiz
    faces = face_detector.detectMultiScale(gray, 1.2, 15)
    #yüz verisinden alacağımız kordinatlara göre bir dikdörtgen çiziyoruz
    for (x, y, w, h) in faces:
        cv2.rectangle(img_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        count += 1
        #verimizi verdiğimiz formatta kaydediyoruz ve kamerayı gösteriyoruz
        cv2.imwrite("pic/" + str(member_name) + '_' + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
        cv2.imshow("frame", img_frame)
    #klavyeden q tuşuna basılınca ya da çekmek istediğimiz fotoğraf sayısı kadar fotoğraf çekildiğinde kapatıyoruz

    if cv2.waitKey(102) & 0xFF == ord('q'):
        break
    elif count > count2:
        break
#pencereyi kapatıyoruz
vid_cam.release()
cv2.destroyAllWindows()
