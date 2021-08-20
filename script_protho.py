import tkinter as tk
import door_control as dc
import client_new as cn
import time
import cv2
import os
from PIL import ImageTk, Image
from tempcheck import tempcheck

tempCurrent = 0
photoTrigger = 0
lavelon = True

#화면 갱신 함수
def reset():
    time_live = time.strftime("%H시 %M분 %S초")
    date_live = time.strftime("%Y년 %m월 %d일")
    timelabel.config(text=date_live+"\n\n"+time_live)
    
    win.after(1000, reset)


def processing():
    global tempCurrent
    global lavelon
    if tempCurrent <= tempcheck() :
                tempCurrent = tempcheck()
    if os.path.isfile('test.jpg'):
        result = "1"
        if tempCurrent <= 37.5 :
            tampcurrent.config(text=str(tempCurrent)+"°C")
            print("정상 체온입니다.")
            result = cn.sendImage()
            set_state(result)
        else :
            statelabel.config(text="체온 이상 감지.\n인증에 실패하였습니다.")
        os.remove('test.jpg')
        trigger_reset()
        win.update()
        label_reset()
    win.after(1000, processing)


def set_state(result) :
    if not result == "1":
        statelabel.config(text="인증되었습니다.")
        print("인증되었습니다.")
        dc.control()
    else :
        statelabel.config(text="인증에 실패하였습니다.")


def trigger_reset():
    global tempCurrent
    global photoTrigger
    tempCurrent = 0
    photoTrigger = 0
    

def label_reset():
    time.sleep(3)
    statelabel.config(text="상태메시지")
    tampcurrent.config(text="°C")

#실시간 화면 송출 및 사진 촬영 함수
def video_play():
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return
    
    #상하반전
    frame = cv2.flip(frame, -1)
    
    photo = frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #얼굴탐색
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
        )
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = frame[y:y+h, x:x+h]
        roi_color = frame[y:y+h, x:x+w]
        
        global photoTrigger
        if photoTrigger != 20 :
            photoTrigger += 1
        else :
            cv2.imwrite('test.jpg', photo)
            photoTrigger += 1
    
    
    global img
    img= Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)

    falselabel.imgtk = imgtk
    falselabel.configure(image=imgtk)
    falselabel.after(10, video_play)



win = tk.Tk()
win.title("출입 시스템")
win.geometry("800x480")
win.resizable(False, False)

#전체화면
win.attributes("-fullscreen", True)
win.bind("<F11>", lambda event: win.attributes("-fullscreen", not win.attributes("-fullscreen")))
win.bind("<Escape>", lambda event: win.attributes("-fullscreen", False))

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

#동영상 프레임
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

#상테 메세지 라벨
statelabel = tk.Label(massegeframe, text="상태메세지")
statelabel.pack(expand="True")

#체온 라벨
tampcurrent = tk.Label(tampframe, text="0°C", font=("times", "25"))
tampcurrent.pack(expand="True")

#OpenCV->Tkinter변환용 라벨
falselabel = tk.Label(cameraframe)
falselabel.grid()

cap = cv2.VideoCapture(-1)
cap.set(3, 300)
cap.set(3, 300)


video_play()
reset()
processing()
#label_reset()

win.mainloop()





