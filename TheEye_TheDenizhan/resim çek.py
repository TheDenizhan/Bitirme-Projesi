import cv2

# Bilgisayarımızın kamerasından alınan görüntüyü değişkene atıyoruz
vid_cam = cv2.VideoCapture("Video_Kayit.mp4")

# Yüz algılama modelimizi yüklüyoruz
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Verilerimizi kaydederken tanımlayacağımız değişkenleri oluşturuyoruz
member_name = "DenizhanHasan"

# Video kaydedici nesnesi oluşturuyoruz
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Video codec
out = cv2.VideoWriter('output_video.mp4', fourcc, 20.0, (480 , 864))  # Ayarları uygun şekilde düzenleyin

# Birden fazla fotoğraf çekeceğimiz için bir döngü oluşturuyoruz
while True:
    # Kameradan aldığımız görüntülerimizi okuyoruz ve gri tonlama uyguluyoruz
    ret, img_frame = vid_cam.read()

    # Görüntü alımı başarısız olursa, döngüden çık
    if not ret:
        print("Görüntü alınamadı veya video sona erdi.")
        break

    gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)

    # Algıladığımız yüz için dikdörtgen çiziyoruz
    faces = face_detector.detectMultiScale(gray, 1.2, 15)
    for (x, y, w, h) in faces:
        cv2.rectangle(img_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Videoya yazıyoruz
    out.write(img_frame)

    # Kamerayı gösteriyoruz
    cv2.imshow("frame", img_frame)

    # Klavyeden q tuşuna basılınca kapatıyoruz
    if cv2.waitKey(102) & 0xFF == ord('q'):
        break

# Video kaydediciyi ve kamerayı kapatıyoruz
out.release()
vid_cam.release()
cv2.destroyAllWindows()
