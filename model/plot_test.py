#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import random
import sys
import os

sys.path.insert(0,'..' + os.sep + 'gui')

file = open(r'..' + os.sep + 'buffer.txt', 'r')
parf=file.read().split(':')

# чтение видео
cap = cv2.VideoCapture(parf[0])
ret, frame = cap.read()
ratio = .5  # коэффициент изменения размера
image = cv2.resize(frame, (0, 0), None, ratio, ratio)  # изменить размер изображения

df = pd.read_csv('..' + os.sep + 'data' + os.sep + 'cout' + os.sep + 'test0.csv')  # читает CSV-файл и делает его фреймом данных
rows, columns = df.shape  # форма данных
print('Rows:     ', rows)
print('Columns:  ', columns)

fig1 = plt.figure(figsize=(10, 8))  # ширина и высота изображения
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # снимает первый кадр видео

for i in range(columns - 1):  # циклически перебирает все столбцы dataframe - 1, так как индекс считается
    y = df.loc[df[str(i)].notnull(), str(i)].tolist()  # получает не нулевые данные из столбца
    df2 = pd.DataFrame(y, columns=['xy'])  # создать другой фрейм данных только с одним столбцом

    # создайте другой фрейм данных, где он разбивает значения центроидов x и y на два столбца
    df3 = pd.DataFrame(df2['xy'].str[1:-1].str.split(',', expand=True).astype(float))
    df3.columns = ['x', 'y','def_type']  # переименовывает столбцы
    print(df3)
    # сюжетные серии со случайными цветами
    plt.plot(df3.x, df3.y, marker='x', color=[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)],
             label=['ID: ' + str(i)])

# plot инфа
plt.title('Tracking of Centroids')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend(bbox_to_anchor=(1, 1.2), fontsize='x-small')  # расположение легенды и шрифт
plt.show()
fig1.savefig('..' + os.sep + 'data' + os.sep + 'cout' + os.sep + 'test0.png')  # сохраняет изображение


import WindowsApp
