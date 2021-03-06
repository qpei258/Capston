import door_control as dc
import pi_client as cn
import time
import cv2
import os
from tempcheck import tempcheck



def processing(img):
    tempCurrent = tampcheck()    
    if tempCurrent < 37.5:
        cv2.imwrite('test.jpg', img)
        result = cn.send_img().split('@')
        cv2.putText(img, result, (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
        cv2.putText(img, str(tempCurrent), (240, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
        else :
        cv2.putText(img, "체온 이상!", (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
        cv2.putText(img, str(tempCurrent), (240, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
    photoTrigger = 0
    if result != ‘안면 인식 실패’:
        dc.door_control()
    return img

def cv_face_check(cap, faceCascade):
    while True:
        if os.path.isfile('test.jpg'):
            os.remove('test.jpg')
            time.sleep(2)
            tempCurrent = 0
        ret, img = cap.read()
        img = cv2.flip(img, -1)
        faces = faceCascade.detectMultiScale(
            img,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_color = img[y:y + h, x:x + w]

            photoTrigger
            print(photoTrigger)
            if photoTrigger != 15:
                photoTrigger += 1
            else:
                process()
        cv2.imshow('video', img)  
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

tempCurrent = 0
photoTrigger = 0

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(-1)
cap.set(3, 480)  # set Width
cap.set(4, 700)  # set Height

