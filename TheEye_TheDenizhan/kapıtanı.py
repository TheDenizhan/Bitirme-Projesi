import cv2



recognizer =cv2.face.LBPHFaceRecognizer.create()

recognizer.read('code/code.yml')
cascadePath="haarcascade_frontalface_default.xml"
faceCascade= cv2.CascadeClassifier(cascadePath)

font= cv2.FONT_HERSHEY_SIMPLEX
cam2= cv2.VideoCapture("tanıma.mp4")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Video codec
out = cv2.VideoWriter('kapiacilis_1.mp4', fourcc, 20.0, (480 , 864))  # Ayarları uygun şekilde düzenleyin
while(True):
    ret,img2=cam2.read()
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,1.2,5)

    for(x,y,w,h) in faces:
        cv2.rectangle(img2,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),4)
        Id,confidence= recognizer.predict(gray[y:y+h,x:x+w])

        if(0<Id and 51>Id):
            Id = "hasan"
            print(Id)
        else:
            Id = "Unknown"
            print(Id)

        cv2.rectangle(img2, (x - 22, y - 90), (x + w + 22, y - 22), (255,0, 0), -1)
        cv2.putText(img2, str(Id), (x, y - 40), font, 2, (255, 255, 255), 3)
    out.write(img2)
    cv2.imshow('img2', img2)

    if cv2.waitKey(10)& 0xFF == ord('q'):
            break

cam2.release()
cv2.destroyAllWindows()