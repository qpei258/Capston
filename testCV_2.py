import door_control as dc
import client_new as cn
import time
import cv2
import os
# from tempcheck import tempcheck
import numpy as np


def processing():
    global tempCurrent
#     if tempCurrent <= tempcheck() :
#             tempCurrent = tempcheck()

    if os.path.isfile('test.jpg') :
        if tempCurrent < 37.5 :
            #result = cn.sendImage().split('@')
            result=''
            result = result.split('@')
            
            

tempCurrent = 0
photoTrigger = 0

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(-1)
cap.set(3,480) # set Width
cap.set(4,700) # set Height
while True:
    if os.path.isfile('test.jpg') :
        os.remove('test.jpg')
        time.sleep(3)
        tempCurrent = 0
        
    ret, img = cap.read()
    img = cv2.flip(img, -1) # 상하반전
    faces = faceCascade.detectMultiScale(
        img,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_color = img[y:y+h, x:x+w]
        
        photoTrigger
        print(photoTrigger)
        if photoTrigger != 15 :
            photoTrigger += 1
        else :
            cv2.imwrite('test.jpg', img)
            processing()
            cv2.putText(img, "testtext", (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
            photoTrigger = 0
            
    cv2.imshow('video',img) # video라는 이름으로 출력
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
        break
    
cap.release()
cv2.destroyAllWindows()

