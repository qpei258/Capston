import door_control as dc
import pi_client as cn
import time
import cv2
import os
from tempcheck import tempcheck



def processing():
    global tempCurrent

# 안면 인식 후 촬영한 사진이 존재하고, 체온 이상이 없다면 서버로 사진을 전송
# 전송 후 서버의 처리 결과를 리턴


tempCurrent = 0
photoTrigger = 0
#체온 및 사진 트리거 초기화

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(-1)
cap.set(3, 480)  # set Width
cap.set(4, 700)  # set Height
#카메라 세팅 및 화면 크기 설정

while True:
    if os.path.isfile('test.jpg'):
        os.remove('test.jpg')
        time.sleep(2)
        tempCurrent = 0
#사진이 존재한다면 사진 파일을 삭제하고 2초 대기=>화면에 2초간 처리 결과를 띄우는 코드
#체온 초기화

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
# 안면 인식 코드

        if photoTrigger != 15:
            photoTrigger += 1
# 사진의 신뢰도를 높이기 위한 트리거. 15프레임 뒤의 사진을 저장하므로써 초점이 맞지 않는 사진이 서버로 전송되는 것을 방지
# 최종적 테스트에서 조정이 필요

        else:
            cv2.imwrite('test.jpg', img)
            if tempCurrent <= tempcheck():
                tempCurrent = tempcheck()
            # tempcheck() 함수를 통해 열화상 카메라에서 체온을 추출하여 tempCurrent에 저장
            # 단 정확도를 높이기 위해 기존에 저장된 체온보다 측정된 온도가 높을 경우에만 현재 체온을 갱신
            # dc.control()
            if os.path.isfile('test.jpg') and tempCurrent < 37.5:
                result = cn.sendImage().split('@')
            cv2.putText(img, result, (240, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
            cv2.putText(img, str(tempCurrent), (240, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0))
            photoTrigger = 0
# 15프레임이 지났다면 해당 프레임을 파일로 저장하고 processing 함수를 진행. 서버의 처리 결과를 화면에 입력

    cv2.imshow('video', img)  #화면에 이미지 출력
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit # ESC를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
