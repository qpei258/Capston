import tkinter as tk
import time
import cv2
from PIL import ImageTk, Image

#화면 갱신 함수
def reset():
    time_live = time.strftime("%H시 %M분 %S초")
    date_live = time.strftime("%Y년 %m월 %d일")
    timelabel.config(text=date_live+"\n\n"+time_live)
    timelabel.after(200, reset)

#실시간 화면 송출 함수
def video_play():
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)

    falselabel.imgtk = imgtk
    falselabel.configure(image=imgtk)
    falselabel.after(10, video_play)


win = tk.Tk()
win.title("출입 시스템")
win.geometry("800x480")
win.resizable(True, True)

#동영상 프레임
cameraframe = tk.Frame(win, relief="groove", width=350, bg="white", bd=2)
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
statelabel =  tk.Label(massegeframe, text="상태메세지")
statelabel.pack(expand="True")


#체온 라벨
tampcurrent = tk.Label(tampframe, text="36.7°C", font=("times", "25"))
tampcurrent.pack(expand="True")

#OpenCV->Tkinter변환용 라벨
falselabel = tk.Label(cameraframe)
falselabel.grid()

cap = cv2.VideoCapture(-1)
cap.set(3, 300)
cap.set(3, 300)


video_play()
reset()

win.mainloop()

