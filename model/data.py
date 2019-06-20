# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from math import sqrt
import sys
sys.path.insert(0,'..\gui')



data=pd.read_csv("../data/cout/test0.csv")
del data['Frames']
data=data.transpose().fillna('0')
data.head()
print(data.shape)

dist=[]
type_idn=[]
idn=[0 for i in range(len(data.index.values))]
for i in range(len(data.index.values)):
  mav1=mav2=0
  miv1=miv2=0
  f=False
  k=0
  typ=[]
  for j in range(len(data.columns.values)):
    if (data.iloc[i][j]!='0') and (f==False):
      typ.append(int(str(data.iloc[i][j].split(',')[2].split(']')[0]).strip()))
      miv1=int(str(data.iloc[i][j].split(',')[0].split('[')[1].split('.')[0]).strip())
      miv2=int(str(data.iloc[i][j].split(',')[1].split('.')[0]).strip())
      k+=1
      del data.iloc[i][j]

    if (data.iloc[i][j]!='0') and (f==True):
      typ.append(int(str(data.iloc[i][j].split(',')[2].split(']')[0]).strip()))
      mav1=int(str(data.iloc[i][j].split(',')[0].split('[')[1].split('.')[0]).strip())
      mav2=int(str(data.iloc[i][j].split(',')[1].split('.')[0]).strip())
      k+=1
      del data.iloc[i][j]
    f=True
  dist.append(sqrt(pow(miv1-miv2,2)+pow(mav1-mav2,2)))
  type_idn.append(round(len(typ)/k))
  idn[i]={dist[i]:type_idn[i]}
  dist[i]=str(int(dist[i]))

data=pd.DataFrame(0,index=list(range(len(idn))),columns=dist)
type_idn=pd.Series(data=type_idn)
np.fill_diagonal(data.values, type_idn)

data.to_csv("../data/cout/out_data.csv")


import WindowsApp
