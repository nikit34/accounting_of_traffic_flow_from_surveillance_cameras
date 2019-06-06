from tkinter import *
import math
from PIL import ImageTk
from PIL import Image
import sys

sys.path.insert(0,'..\model')
sys.path.insert(0,'..\data\cin')
global pathf


def traffic_(pathf):
    try:
        pathf=pathf
        print(pathf)
        import traffic_test
    except ImportError:
        print('ImportError in traffic')


def plot_(pathf):
    try:
        import plot_test
    except:
        print('Error in plot')


def map_():
    try:
        import map_test
    except:
        print('Error in map')


def data_():
    try:
        import data
    except:
        print('Error in data')

def butd(pf,bu1,bu2):

    pathf='../cin/'+pf
    global image1
    image1=ImageTk.PhotoImage(file="СТАРТ1.png")
    button1=Button(bu1, image=image1, bg='gray', borderwidth=2, relief="raised", command=lambda:traffic_(str(pathf)))
    button1.place(relx=0,rely=0,relwidth=1,relheight=1)
    global image2
    image2=ImageTk.PhotoImage(file="ТРАЕКТОРИЯ.png")
    button2=Button(bu2, image=image2, bg='gray', borderwidth=2, relief="raised", command=lambda:plot_(pathf))
    button2.place(relx=0,rely=0,relwidth=1,relheight=1)

def main():
    root=Tk()
    root.title('Air-fresh')

    _H=600
    _W=1200

    canvas=Canvas(root,height=_H, width=_W)
    fon = PhotoImage(file='fon.png')
    fon_l = Label(root, image=fon)
    fon_l.place(relx=0, rely=0, relwidth=1, relheight=1)
    canvas.pack()

    panel=Frame(root,bg='white', bd=5, relief="groove")
    panel.place(relx=0.1,rely=0.03,relwidth=0.803,relheight=0.1)

    bu1=Label(root, text="введите", bg='gray', borderwidth=2, relief="raised")
    bu1.place(relx=0.105,rely=0.04,relwidth=0.22,relheight=0.08)
    bu2=Label(root, text="путь", bg='gray', borderwidth=2, relief="raised")
    bu2.place(relx=0.325,rely=0.04,relwidth=0.175,relheight=0.08)

    image3=ImageTk.PhotoImage(file="КАРТА.png")
    button3=Button(root, image=image3, bg='gray', borderwidth=2, relief="raised", command=lambda:map_())
    button3.place(relx=0.5,rely=0.04,relwidth=0.175,relheight=0.08)
    image4=ImageTk.PhotoImage(file="ДАННЫЕ1.png")
    button4=Button(root, image=image4, bg='gray', borderwidth=2, relief="raised", command=lambda:data_())
    button4.place(relx=0.675,rely=0.04,relwidth=0.22,relheight=0.08)

    entry = Entry(root, font=40)
    entry.place(relx=0.105,rely=0.15,relwidth=0.15, relheight=0.04)

    image5=ImageTk.PhotoImage(file="ЗАГРУЗИТЬ.png")
    button5=Button(root, image=image5, bg='gray', borderwidth=2, relief="raised", command=lambda:butd(str(entry.get()),bu1,bu2))
    button5.place(relx=0.255,rely=0.15,relwidth=0.07,relheight=0.04)
    root.mainloop(n=0)



if __name__=="__main__":
    main()
