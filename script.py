# -*- coding: utf8 -*- 
import tkinter as tk
from tempcheck import tempcheck
import time


#시간 설정 함수
def reset():
    time_live = time.strftime("%H시 %M분 %S초")
    date_live = time.strftime("%Y년 %m월 %d일")
    timelabel.config(text=date_live+"\n\n"+time_live)
#     timelabel.after(1000, reset)
#체온 설정 함수
    tampcurrent.config(text=str(tempcheck())+"°C")
    win.after(1000, reset)

win = tk.Tk()
win.title("출입 시스템")
win.geometry("500x300+50+50")
win.resizable(True, True)

#동영상 프레임
cameraframe = tk.Frame(win, relief="groove", width=350, bg="white", bd=2)
cameraframe.pack(side="right", fill="both", expand=True)

#텍스트 프레임
dateframe = tk.Frame(win, relief="groove", width=150, height=50, bd=2)
dateframe.pack(side="top", fill="both", expand=True)
dateframe.propagate(0)
tampframe = tk.Frame(win, relief="groove", width=150, height=50, bd=2)
tampframe.pack(fill="both", expand=True)
tampframe.propagate(0)
massegeframe = tk.Frame(win, relief="groove", width=150, height=50, bd=2)
massegeframe.pack(side="bottom", fill="both", expand=True)
massegeframe.propagate(0)

#시간 라벨
timelabel = tk.Label(dateframe, text="", font=("times", "14"))
timelabel.pack(expand="True")

#상테 메세지 라벨
statelabel =  tk.Label(massegeframe, text="상태메세지")
statelabel.pack(expand="True")

#체온 라벨
tampcurrent = tk.Label(tampframe, text="0°C", font=("times", "25"))
tampcurrent.pack(expand="True")


reset()

win.mainloop()

