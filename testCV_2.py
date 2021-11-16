import door_control as dc
import pi_client as cn
import time
import cv2
import os
from tempcheck import tempcheck



def processing(img):
    cv2.imwrite('test.jpg', img)
    tempCurrent = tampcheck()
    
    if os.path.isfile('test.jpg') and tempCurrent < 37.5:
        result = cn.send_img().split('@')
        cv2.putText(img, result, (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
        cv2.putText(img, str(tempCurrent), (240, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
    else :
        cv2.putText(img, "체온 이상!", (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
        cv2.putText(img, str(tempCurrent), (240, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
    photoTrigger = 0
    dc.door_control()
    return img
    
# 안면 인식 후 촬영한 사진이 존재하고, 체온 이상이 없다면 서버로 사진을 전송
# 전송 후 서버의 처리 결과를 리턴

def cv_face_check(cap, faceCascade):
    while True:
        if os.path.isfile('test.jpg'):
            os.remove('test.jpg')
            time.sleep(2)
            tempCurrent = 0
        ret, img = cap.read()
        img = cv2.flip(img, -1)  # 상하반전
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
        cv2.imshow('video', img)  #화면에 이미지 출력
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit # ESC를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()

tempCurrent = 0
photoTrigger = 0

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(-1)
cap.set(3, 480)  # set Width
cap.set(4, 700)  # set Height

