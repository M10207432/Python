import os, sys

import numpy as np
from numpy import *

from collections import OrderedDict
from grs import Stock
from grs import TWSENo

import cPickle as pickle
import matplotlib.pyplot as plt

def readStockdata(filename):
  result_list = []
  buy_date=''
  
  readobj = open(filename, 'rb')
  content = readobj.read()
  readobj.close()

  rowlist = content.split('\n')
  
  for i,row in enumerate(rowlist):
    if i==0:
      buy_date = row 
    if i != 0 and row.strip():
      result_list.append(map(eval, row.split(',')))
  
  return buy_date,mat(result_list)


def calProb(stockmap):
  buylist=[]
  win_prob = 1.0
  lose_prob = 1.0
  
  for r in stockmap:
    if r[0,3] > 0.85 and r[0,1]!=0:
      buylist.append(r)
      win_prob = win_prob * r[0,3] 
      lose_prob = lose_prob * (1.0 - r[0,3]) 

  #print buylist
  #print "Win:",win_prob
  #print "Lose:",lose_prob
  return buylist

def Tracing(buy_date, stockmap):  #row[Stock_id, Stock dollar $, Training Probility, Test Probility]

  Earn=0
  draw_x=[]
  draw_y=[]
  draw_yn=[]
  
  for row in stockmap:
    stock_id = str(int(row[0,0]))
    s = Stock(stock_id,1)

    
    nowlist = s.raw[len(s.raw) - 1]
    now_dollar = float(nowlist[6])
    buy_dollar = float(row[0,1])
    diff = (now_dollar - buy_dollar)
    print "Stock %s %s, %f (Buy:%f)=>%f" % (stock_id, s.info[1], now_dollar, buy_dollar, diff)
    
    Earn = Earn + diff
    
    draw_x.append(stock_id)
    draw_y.append(buy_dollar)
    draw_yn.append(now_dollar)
  print "Now Stock Earn=%f !!!" % (Earn)
  print "Now $ Earn=%f !!!" % (Earn*1000)
  '''
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(draw_x, draw_yn, c='blue',marker='o')
  ax.scatter(draw_x, draw_y, c='green',marker='o')
  ax.plot()
  plt.show()
  '''
def main():
  buy_date, stockmap = readStockdata('2017-03-03.txt')
  buylist = calProb(stockmap)
  Tracing(buy_date, buylist)
  

if __name__=="__main__":
  main()

