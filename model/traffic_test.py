import numpy as np
import cv2
import pandas as pd
import sys
import os

sys.path.insert(0,'..' + os.sep + 'gui')
file = open(r'..' + os.sep + 'buffer.txt', 'r')
parf=file.read().split(':')

print(parf[0])
# чтение видео
cap = cv2.VideoCapture(str(parf[0]))
# CAP_PROP_FRAME_COUNT - количество кадров в видео
frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS), cap.get(
    cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# разрешение кадров - одинаковое в видео
width = int(width)
height = int(height)
print('**************************************************************')
print('******************** Параметры видео *************************')
print('* Количество кадров:                                    ', frames_count)
print('* FPS:                                                  ', fps)
print('* разрешение:                                 ' ,width, ' x ' ,height, ' px')
print('* Продолжительность:                                 ' ,int(frames_count/fps),' мин.')
print('**************************************************************')

# создает фрейм данных pandas с количеством строк такой же длины, что и количество кадров
df = pd.DataFrame(index=range(int(frames_count)))
df.index.name = "Frames"
f=0

framenumber = 0  # отслеживает текущий кадр
carscrossedup = 0  # количество автомобилей, пересекающих верхнюю линию
carscrosseddown = 0  # количество автомобилей, пересекающих нижнюю линию
carids = []  # пустой список для добавления id автомобилей
caridscrossed = []  # id автомобилей, пересёкших линию
totalcars = 0  # общее количество автомобилей

fgbg = cv2.createBackgroundSubtractorMOG2()  # фон, который будет вычитаться от детект. объекта

# блок для сохранения видео - не обязательный
ret, frame = cap.read()  # чтение
ratio = .5
image = cv2.resize(frame, (0, 0), None, ratio, ratio)  # сжатие видео на коэффициент ratio
width2, height2, channels = image.shape
# запись
video = cv2.VideoWriter('..' + os.sep + 'data' + os.sep + 'cout' + os.sep + 'test0.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (height2, width2), 1)
video_text = cv2.VideoWriter('..' + os.sep + 'data' + os.sep + 'cout' + os.sep + 'testtext0.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (700,700), 1)

while True:
    ret, frame = cap.read()
    if ret:
        image = cv2.resize(frame, (0, 0), None, ratio, ratio)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # конвектировать в ч/б
        fgmask = fgbg.apply(gray)  # применение ч/б

        # применяет различные пороги к fgmask, чтобы попытаться изолировать автомобили
        # !!! настраивать параметры вручную !!!
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # применение морфологического ядра
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel)
        retvalbin, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)  # удаление теней по ядру

        # создать контур
        contours, hierarchy = cv2.findContours(bins, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # использовать выпуклый корпус для создания многоугольника вокруг контуров
        hull = [cv2.convexHull(c) for c in contours]

        # рисовать контуры
        cv2.drawContours(image, hull, -1, (0, 255, 0), 3)

        # линия, созданная для прекращения подсчета контуров, необходимая, поскольку автомобили на
        # расстоянии становятся одним большим контуром
        # на высоте n% от верхней грани



        #---------------------------------------------------------------------------------------------
        """ Есть две линии. Пусть машины движутся от нас, тога пересекают сначала нижнюю линию.
            Когда кариды(контуры) близки к центройду - засекаем в прямоугольник, и
            увеличиваем счетчик машин на этой линии. Зеленая линия маргнет красным в этот момент.
            Пересекает вторую линию - прекращаем следить.
            Здесь синия полоса всегда выше зеленной,
            и на местности она 'дальше'. Обратная ситуация не зеркальна.
        """
        # верхняя (синия) линия - граница наблюдения
        lineypos = int(height * 0.05)
        cv2.line(image, (0, lineypos), (width, lineypos), (255, 0, 0), 5)

        # нижняя линия (зелено - красная), создана для счёта
        lineypos2 = int(height * 0.4)
        cv2.line(image, (0, lineypos2), (width, lineypos2), (0, 255, 0), 5)


        # минимальная площадь для контуров в случае выявления группы небольших контуров шума
        # minarea = 2570
        minarea =int(parf[1])
        # максимальная площадь для контуров, может быть довольно большой для автобусов
        maxbus = 10000
        maxcar = 5420

        # максимально допустимый радиус для текущего центроида кадра, который будет считаться таким же центроидом из предыдущего кадра
        # maxrad = 15
        maxrad = int(parf[2])
        #---------------------------------------------------------------------------------------------



        # векторы для координатных центроидов x и y в текущем кадре
        cxx = np.zeros(len(contours))
        cyy = np.zeros(len(contours))

        for i in range(len(contours)):  # циклически перебирает все контуры в текущем кадре
            if hierarchy[0, i, 3] == -1:  # использование иерархии для подсчета только родительских контуров (контуры не внутри других)

                area = cv2.contourArea(contours[i])  # площадь контура
                if minarea < area < maxbus:  # порог площади для контура
                    if maxcar < area:
                        f=2
                    else:
                        f=1

                    # расчет центроидов контуров
                    cnt = contours[i]
                    M = cv2.moments(cnt)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    if cy > lineypos:  # отфильтровывает контуры, которые находятся выше линии (у - начинается сверху)

                        # получает ограничивающие точки контура для создания прямоугольника
                        # x, y - верхний левый угол, а w, h - ширина и высота.
                        x, y, w, h = cv2.boundingRect(cnt)

                        # создает прямоугольник вокруг контура
                        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                        # Печатает метку центроида (текст), чтобы позже проверить
                        cv2.putText(image, str(cx) + "," + str(cy), (cx + 10, cy + 10),cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 0, 255), 1)

                        cv2.drawMarker(image, (cx, cy), (0, 0, 255), cv2.MARKER_STAR, markerSize=5, thickness=1, line_type=cv2.LINE_AA)

                        # добавляет центроиды, которые прошли предыдущие критерии в список центроидов
                        cxx[i] = cx
                        cyy[i] = cy

        # сокращает элементы, равные нулю
        cxx = cxx[cxx != 0]
        cyy = cyy[cyy != 0]

        # пустой список, чтобы позже проверить, какие индексы центроида были добавлены в датафрейм
        minx_index2 = []
        miny_index2 = []

        # Раздел ниже отслеживает центроиды и назначает их старым каридам или новым каридам.

        if len(cxx):  # если это центроид отмеченный

            if not carids:  # если лист каридов пустой

                for i in range(len(cxx)):  # проходит через все центройды

                    carids.append(i)  # добавляет id машины в пустой лист
                    df[str(carids[i])] = ""  # добавляет в датафрейм колонки по id

                    # присваивает значения центроида текущему кадру (строке) и кариде (столбцу)
                    df.at[int(framenumber), str(carids[i])] = [cxx[i], cyy[i],f]

                    totalcars = carids[i] + 1  # добавляет к общему количеству автомобилей

            else:  # если уже есть идентификаторы автомобилей

                # новые массивы для расчета дельт
                dx = np.zeros((len(cxx), len(carids)))
                dy = np.zeros((len(cyy), len(carids)))

                for i in range(len(cxx)):  # проходит через все центроиды

                    for j in range(len(carids)):  # проходит через все записанные id автомобилей

                        # приобретает центр тяжести из предыдущего кадра для определенного карида
                        oldcxcy = df.iloc[int(framenumber - 1)][str(carids[j])]

                        # получает текущий центр тяжести кадра, который не обязательно совпадает с предыдущим кадром кадра
                        curcxcy = np.array([cxx[i], cyy[i]])

                        if not oldcxcy:  # проверяет, пуст ли старый центроид в случае, если автомобиль покидает экран, и новый автомобиль показывает

                            continue  # продолжить следующий карид

                        else:  # посчитать разницу по сравнению с предыдущими каридами

                            dx[i, j] = oldcxcy[0] - curcxcy[0]
                            dy[i, j] = oldcxcy[1] - curcxcy[1]

                for j in range(len(carids)):  # проходит через все текущие идентификаторы автомобилей

                    sumsum = np.abs(dx[:, j]) + np.abs(dy[:, j])  # суммирует дельты в отношении id автомобилей

                    # находит, какой индекс карид имел минимальную разницу, и это истинный индекс
                    correctindextrue = np.argmin(np.abs(sumsum))
                    minx_index = correctindextrue
                    miny_index = correctindextrue

                    # получает минимальную дельту
                    mindx = dx[minx_index, j]
                    mindy = dy[miny_index, j]

                    if mindx == 0 and mindy == 0 and np.all(dx[:, j] == 0) and np.all(dy[:, j] == 0):
                        # проверяет на полноту нулей карид

                        continue  # следующий карид
                    else:

                        # если дельта меньше допустимого радиуса - добавить центроид в карид
                        if np.abs(mindx) < maxrad and np.abs(mindy) < maxrad:

                            # добавляет центроид к соответствующему ранее существующему кариду
                            df.at[int(framenumber), str(carids[j])] = [cxx[minx_index], cyy[miny_index],f]
                            minx_index2.append(minx_index)  # добавляет все индексы, которые были добавлены к предыдущим каридам
                            miny_index2.append(miny_index)

                for i in range(len(cxx)):  # проходит через все центроиды

                    # если центроида нет в списке минииндекса, нужно добавить еще одну машину
                    if i not in minx_index2 and miny_index2:

                        df[str(totalcars)] = ""  # создать еще одну колонку с общим количеством автомобилей
                        totalcars = totalcars + 1  # добавляет еще один общий счетчик
                        t = totalcars - 1  # заполнитель для общего количества машин
                        carids.append(t)  # добавляет id машины
                        df.at[int(framenumber), str(t)] = [cxx[i], cyy[i],f]  # добавляет центроид в карид

                    elif curcxcy[0] and not oldcxcy and not minx_index2 and not miny_index2:
                        # если предыдущий центроид не был в кариде
                        # новая машина будет добавлена если карид пуст

                        df[str(totalcars)] = ""  # создать колонку с общим количеством автомобилей
                        totalcars = totalcars + 1  # +1 в общий счетчик
                        t = totalcars - 1  # t - заполнитель
                        carids.append(t)  # добавить в список id
                        df.at[int(framenumber), str(t)] = [cxx[i], cyy[i],f]  # добавить центроид новой машины

        # раздел ниже помечает центриды на экране
        currentcars = 0  # текущие автомобили на экране
        currentcarsindex = []  # текущие автомобили на экране Carid Index

        for i in range(len(carids)):  # проходит через все кариды

            if df.at[int(framenumber), str(carids[i])] != '':
                # проверяет есть ли корректные кариды, не равные пустому знач.

                currentcars = currentcars + 1  # добавляет другую машину на экране
                currentcarsindex.append(i)  # добавляет id этой машины

        for i in range(currentcars):  # перебирает все текущие идентификаторы автомобилей на экране

            # захватывает центр тяжести определенного карида для текущего кадра
            curcent = df.iloc[int(framenumber)][str(carids[currentcarsindex[i]])][:-1]

            # захватывает центр тяжести определенного карида за предыдущий кадр
            oldcent = df.iloc[int(framenumber - 1)][str(carids[currentcarsindex[i]])][:-1]

            if curcent:  # если центроид корректный

                # текст на экране для текущего карида
                cv2.putText(image, "C*d:" + str(curcent[0]) + "," + str(curcent[1]),
                            (int(curcent[0]), int(curcent[1])), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1)

                cv2.putText(image, "ID:" + str(carids[currentcarsindex[i]])+' '+str('car' if f==1 else 'bus'), (int(curcent[0]), int(curcent[1] - 15)),
                            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1)

                # рисуется метка
                cv2.drawMarker(image, (int(curcent[0]), int(curcent[1])), (0, 0, 255), cv2.MARKER_STAR, markerSize=5, thickness=1, line_type=cv2.LINE_AA)

                if oldcent:  # если сатый центорид существует
                    # добавляет радиус из предыдущего центроида в текущий центроид для визуализации
                    xstart = oldcent[0] - maxrad
                    ystart = oldcent[1] - maxrad
                    xwidth = oldcent[0] + maxrad
                    yheight = oldcent[1] + maxrad
                    cv2.rectangle(image, (int(xstart), int(ystart)), (int(xwidth), int(yheight)), (0, 125, 0), 1)

                    # проверяет, находится ли старый центроид на линии или ниже линии, а курс на линии или выше линии
                    # считать автомобили, и эта машина еще не была учтена
                    if oldcent[1] >= lineypos2 and curcent[1] <= lineypos2 and carids[
                        currentcarsindex[i]] not in caridscrossed:

                        carscrossedup = carscrossedup + 1
                        cv2.line(image, (0, lineypos2), (width, lineypos2), (0, 0, 255), 5)

                        # добавляет id машины в список машин, чтобы избежать двойного счета
                        caridscrossed.append(currentcarsindex[i])

                    # проверяет, находится ли старый центроид на верхней линии или выше, а курс - на нижний линии или ниже
                    # считать автомобили, и эта машина еще не была учтена
                    elif oldcent[1] <= lineypos2 and curcent[1] >= lineypos2 and carids[
                        currentcarsindex[i]] not in caridscrossed:

                        carscrosseddown = carscrosseddown + 1
                        cv2.line(image, (0, lineypos2), (width, lineypos2), (0, 0, 125), 5)
                        caridscrossed.append(currentcarsindex[i])


        field_t = np.zeros((700, 700, 3), np.uint8)



        # Текст в левом верхнем углу прямоугольника
        cv2.rectangle(field_t, (0, 0), (700, 700), (255, 255, 255), -1)  # фоновый прямоугольник для текста на экране

        cv2.putText(field_t, '******************** Video options ***************************', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)
        cv2.putText(field_t, "* Cars in Area: " + str(currentcars), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, "* Cars Crossed Up: " + str(carscrossedup), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0),
                   2)

        cv2.putText(field_t, "* Cars Crossed Down: " + str(carscrosseddown), (0, 80), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    (0, 0, 0), 2)

        cv2.putText(field_t, "* Total Object Detect: " + str(len(carids)), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, .7,
                    (0, 0, 0), 2)

        cv2.putText(field_t, "* Frame: " + str(framenumber) + ' of ' + str(frames_count), (0, 120), cv2.FONT_HERSHEY_SIMPLEX,
                    .7, (0, 0, 0), 2)

        cv2.putText(field_t, '* Time: ' + str(round(framenumber / fps, 2)) + ' sec of ' + str(round(frames_count / fps, 2))
                    + ' sec', (0, 140), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, '* Definable type: ' + str('car' if f==1 else '') + str('bus' if f==2 else ''), (0, 160), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, '**************************************************************', (0, 180), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, '* Number of frames:                      '+str(frames_count), (0, 200), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, '* FPS:                                    '+str(fps), (0, 220), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, '* Permittance:                         '+str(width)+' x '+str(height)+' px', (0, 240), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)

        cv2.putText(field_t, '*                        _________Team of "Air force"_________' , (0, 270), cv2.FONT_HERSHEY_SIMPLEX, .7, (100, 100, 0), 1)

        cv2.putText(field_t, '**************************************************************', (0, 300), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)


        # отображает изображения и преобразования
        cv2.imshow("countours", image)
        cv2.moveWindow("countours", 0, 0)

        cv2.imshow("fgmask", fgmask)
        cv2.moveWindow("fgmask", int(height * ratio)+20, 0)

        cv2.imshow("closing", closing)
        cv2.moveWindow("closing", 0, int(height * ratio))

        cv2.imshow("opening", opening)
        cv2.moveWindow("opening", int(height * ratio)+20, int(height * ratio))

        cv2.imshow("dilation", dilation)
        cv2.moveWindow("dilation", 0, 2*int(height * ratio))

        cv2.imshow("binary", bins)
        cv2.moveWindow("binary",int(height * ratio)+20, 2*int(height * ratio))

        cv2.imshow("field text", field_t)
        cv2.moveWindow("field text", 3*int(height * ratio)-100, 0)

        video.write(image)  # сохранить текущее изображение в видеофайл
        video_text.write(field_t)

        # увеличить число кадров
        framenumber = framenumber + 1

        k = cv2.waitKey(int(1000/fps)) & 0xff  # int(1000/fps) нормальная скорость, так как waitkey в мс
        if k == 27:
            break

    else:  # если видео закончено, то разрыв цикла

        break

cap.release()
cv2.destroyAllWindows()

# сохраняет фрейм данных в CSV-файл для последующего анализа
df.to_csv('..' + os.sep + 'data' + os.sep + 'cout' + os.sep + 'test0.csv', sep=',')
