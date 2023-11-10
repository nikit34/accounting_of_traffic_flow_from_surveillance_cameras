from tkinter import *
import math
from PIL import ImageTk
from PIL import Image
import sys
import os

sys.path.insert(0,'..' + os.sep + 'model')

global pathf
global f

def writestr(pathf,flag):
    f = open(r'..' + os.sep + 'buffer.txt', 'w', encoding='utf-8')
    f.write(str(pathf))
    f.close()
    if flag==True:
        traffic_(pathf)
    else:
        plot_(pathf)


def traffic_(pathf):
    try:
        import traffic_test
    except ImportError as e:
        print('ImportError in traffic ', e)


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

def butd(pf,bu1,bu2,pan1,pan2,pan3,pan4):
    pathf='..' + os.sep + 'data' + os.sep + 'cin' + os.sep + pf+':'+pan1+':'+pan2+':'+pan3+':'+pan4
    global image1
    image1=ImageTk.PhotoImage(file="СТАРТ1.png")
    button1=Button(bu1, image=image1, bg='gray', borderwidth=2, relief="raised", command=lambda:writestr(pathf,True))
    button1.place(relx=0,rely=0,relwidth=1,relheight=1)
    global image2
    image2=ImageTk.PhotoImage(file="ТРАЕКТОРИЯ.png")
    button2=Button(bu2, image=image2, bg='gray', borderwidth=2, relief="raised", command=lambda:writestr(pathf,False))
    button2.place(relx=0,rely=0,relwidth=1,relheight=1)


def main():
    root=Tk()
    root.title('Air-fresh')

    _H=300
    _W=600

    canvas=Canvas(root,height=_H, width=_W)
    fon = PhotoImage(file='fon.png')
    fon_l = Label(root, image=fon)
    fon_l.place(relx=0, rely=0, relwidth=1, relheight=1)
    canvas.pack()

    panel=Frame(root,bg='white', bd=5, relief="groove")
    panel.place(relx=0.1,rely=0.03,relwidth=0.803,relheight=0.1)

    image0=ImageTk.PhotoImage(file="Пустая.png")
    bu1=Label(root, image=image0, bg='gray', borderwidth=2, relief="raised")
    bu1.place(relx=0.105,rely=0.04,relwidth=0.22,relheight=0.08)
    bu2=Label(root, image=image0, bg='gray', borderwidth=2, relief="raised")
    bu2.place(relx=0.325,rely=0.04,relwidth=0.175,relheight=0.08)

    image3=ImageTk.PhotoImage(file="КАРТА.png")
    button3=Button(root, image=image3, bg='gray', borderwidth=2, relief="raised", command=lambda:map_())
    button3.place(relx=0.5,rely=0.04,relwidth=0.175,relheight=0.08)
    image4=ImageTk.PhotoImage(file="ДАННЫЕ1.png")
    button4=Button(root, image=image4, bg='gray', borderwidth=2, relief="raised", command=lambda:data_())
    button4.place(relx=0.675,rely=0.04,relwidth=0.22,relheight=0.08)

    entry = Entry(root, font=20)
    entry.place(relx=0.105,rely=0.15,relwidth=0.15, relheight=0.04)

    pan=Label(root, bg='blue', borderwidth=2, relief="raised")
    pan.place(relx=0.105,rely=0.22,relwidth=0.15,relheight=0.3)

    entry01 = Entry(pan, font=8)
    entry01.place(relx=0.1, rely=0.07,relwidth=0.4, relheight=0.14)
    t01=Label(pan,text='MIN AREA')
    t01.place(relx=0.55, rely=0.09,relwidth=0.45, relheight=0.1)

    entry02 = Entry(pan, font=8)
    entry02.place(relx=0.1,rely=0.3,relwidth=0.4, relheight=0.14)
    t02=Label(pan,text='MAX BUS')
    t02.place(relx=0.55, rely=0.32,relwidth=0.45, relheight=0.1)

    entry03 = Entry(pan, font=8)
    entry03.place(relx=0.1,rely=0.535,relwidth=0.4, relheight=0.14)
    t03=Label(pan,text='MAX CAR')
    t03.place(relx=0.55, rely=0.555,relwidth=0.45, relheight=0.1)

    entry04 = Entry(pan, font=8)
    entry04.place(relx=0.1,rely=0.77,relwidth=0.4, relheight=0.14)
    t04=Label(pan,text='RAD CENT')
    t04.place(relx=0.55, rely=0.79,relwidth=0.45, relheight=0.1)

    image5=ImageTk.PhotoImage(file="ЗАГРУЗИТЬ.png")
    button5=Button(root, image=image5, bg='gray', borderwidth=2, relief="raised", command=lambda:butd(str(entry.get()),bu1,bu2,str(entry01.get()),str(entry02.get()),str(entry03.get()),str(entry04.get())))
    button5.place(relx=0.255,rely=0.15,relwidth=0.07,relheight=0.04)

    root.mainloop(n=0)

if __name__=="__main__":
    main()
