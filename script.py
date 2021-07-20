import tkinter as tk
import time
import cv2
import os
from PIL import ImageTk, Image

#화면 갱신 함수
def reset():
    time_live = time.strftime("%H? %M? %S?")
    date_live = time.strftime("%Y? %m? %d?")
    timelabel.config(text=date_live+"\n\n"+time_live)
    timelabel.after(200, reset)

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
        
        cv2.imwrite('test.jpg', photo)
    
    
    global img
    img= Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)

    falselabel.imgtk = imgtk
    falselabel.configure(image=imgtk)
    falselabel.after(10, video_play)



win = tk.Tk()
win.title("?? ???")
win.geometry("800x480")
win.resizable(False, False)

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


#상태 메시지 라벨
statelabel =  tk.Label(massegeframe, text="?????")
statelabel.pack(expand="True")


#체온라벨
tampcurrent = tk.Label(tampframe, text="36.7�C", font=("times", "25"))
tampcurrent.pack(expand="True")

#OpenCV->Tkinter변환용 라벨
falselabel = tk.Label(cameraframe)
falselabel.grid()

cap = cv2.VideoCapture(-1)
cap.set(3, 300)
cap.set(3, 300)


video_play()
if os.path.isfile('test.jpg'):
    time.sleep(2)

reset()


win.mainloop()





