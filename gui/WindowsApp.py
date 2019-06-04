import tkinter as tk
from math import *
from PIL import ImageTk
from PIL import Image
import sys

sys.path.insert(0,'../model')
sys.path.insert(0,'../data/cin')


def traffic_(pathf):
    try:
        from traffic import *
    except:
        print('Error in traffic')


def plot_(pathf):
    try:
        from plot_test import *
    except:
        print('Error in plot')


def map_():
    try:
        from map_test import *
    except:
        print('Error in map')


def data_():
    try:
        from data import *
    except:
        print('Error in data')


def main():
    root=tk.Tk()
    root.title('Air-fresh')

    _H=600
    _W=1200
    pathf='../cin/'

    canvas=tk.Canvas(root,height=_H, width=_W)
    fon = tk.PhotoImage(file='fon.png')
    fon_l = tk.Label(root, image=fon)
    fon_l.place(relx=0, rely=0, relwidth=1, relheight=1)
    canvas.pack()

    panel=tk.Frame(root,bg='white', bd=5, relief="groove").place(relx=0.1,rely=0.03,relwidth=0.803,relheight=0.1)
    image1=ImageTk.PhotoImage(file="СТАРТ1.png")
    button1=tk.Button(root, image=image1, bg='gray', borderwidth=2, relief="raised", command=lambda:traffic_(pathf)).place(relx=0.105,rely=0.04,relwidth=0.22,relheight=0.08)
    image2=ImageTk.PhotoImage(file="ТРАЕКТОРИЯ.png")
    button2=tk.Button(root, image=image2, bg='gray', borderwidth=2, relief="raised", command=lambda:plot_(pathf)).place(relx=0.325,rely=0.04,relwidth=0.175,relheight=0.08)
    image3=ImageTk.PhotoImage(file="КАРТА.png")
    button3=tk.Button(root, image=image3, bg='gray', borderwidth=2, relief="raised", command=lambda:map_()).place(relx=0.5,rely=0.04,relwidth=0.175,relheight=0.08)
    image4=ImageTk.PhotoImage(file="ДАННЫЕ1.png")
    button4=tk.Button(root, image=image4, bg='gray', borderwidth=2, relief="raised", command=lambda:data_()).place(relx=0.675,rely=0.04,relwidth=0.22,relheight=0.08)

    entry = tk.Entry(root, font=40)
    entry.place(relx=0.105,rely=0.15,relwidth=0.15, relheight=0.04)

    image5=ImageTk.PhotoImage(file="ЗАГРУЗИТЬ.png")
    button5=tk.Button(root, image=image5, bg='gray', borderwidth=2, relief="raised", command=lambda:configure(pathf='../cin/'+entry.get())).place(relx=0.255,rely=0.15,relwidth=0.07,relheight=0.04)

    root.mainloop(n=0)


if __name__=="__main__":
    main()
