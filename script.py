import tkinter as tk
import time
import cv2
import os
import client_new as c
from PIL import ImageTk, Image
from tempcheck import tempcheck

tempCurrent = 0
photoTrigger = 0

#시간 및 체온 갱신 함수
def reset():
    time_live = time.strftime("%H시 %M분 %S초")
    date_live = time.strftime("%Y년 %m월 %d일")
    timelabel.config(text=date_live+"\n\n"+time_live)

    if tempcheck() >= tempCurrent:
        tempCurrent = tempcheck()
    tampcurrent.config(text=str(tempCurrent) + "°C")
    win.after(1000, reset)


# 실시간 화면 송출 및 사진 촬영 함수
def video_play():
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return

    # 상하반전
    frame = cv2.flip(frame, -1)

    photo = frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 얼굴탐색
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = frame[y:y + h, x:x + h]
        roi_color = frame[y:y + h, x:x + w]

        if photoTrigger != 10 :
            photoTrigger += 1
        else :
            cv2.imwrite('test.jpg', photo)
            if os.path.isfile('test.jpg'):
                time.sleep(0.5)


def processing():
    if os.path.isfile('test.jpg'):
        if tempCurrent < 37.5 :
            print("정상 체온입니다.")
            #        result = c.send_image()
            #        os.remove('test.jpg')
            set_state(result)
            trigger_reset()
        else :
            statelabel.config(text="체온 이상 감지.\n인증에 실패하였습니다.")
            time.sleep(1.5)
            trigger_reset()
    win.after(1000, processing)

def door_control() :
#서보모터 처리
    trigger_reset()


def set_state(result) :
    if result == 1:
        statelabel.config(text="인증되었습니다.")
        door_control()
        time.sleep(1.5)
    else :
        statelabel.config(text="인증에 실패하였습니다.")
    time.sleep(1.5)


def trigger_reset():
    tempCurrent = 0
    photoTrigger = 0
    statelabel.config(text="")

#tkinter
win = tk.Tk()
win.title("출입 시스템")
win.geometry("800x480")
win.resizable(False, False)

#안면인식
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

#카메라 프레임
cameraframe = tk.Frame(win, relief="groove", width=350, height=300, bg="white", bd=2)
cameraframe.pack(side="right", fill="both", expand=True)

#텍스트 프레임
dateframe = tk.Frame(win, relief="groove", width=250, height=50, bd=2)
dateframe.pack(side="top", fill="both", expand=True)
dateframe.propagate(0)

tampframe = tk.Frame(win, relief="groove", width=250, height=50, bd=2)
tampframe.pack(fill="both", expand=True)
tampframe.propagate(0)

massegeframe = tk.Frame(win, relief="groove", width=250, height=50, bd=2)
massegeframe.pack(side="bottom", fill="both", expand=True)
massegeframe.propagate(0)

#시간 라벨
timelabel = tk.Label(dateframe, text="", font=("times", "14"))
timelabel.pack(expand="True")

#상태 메시지 라벨
statelabel =  tk.Label(massegeframe, text="상태 메시지")
statelabel.pack(expand="True")

#체온라벨
tampcurrent = tk.Label(tampframe, text=str(tempCurrent)+ "°C", font=("times", "25"))
tampcurrent.pack(expand="True")

#OpenCV->Tkinter변환용 라벨
falselabel = tk.Label(cameraframe)
falselabel.grid()

#카메라 세팅
cap = cv2.VideoCapture(-1)
cap.set(3, 300)
cap.set(3, 300)

video_play()
reset()
processing()


win.mainloop()
