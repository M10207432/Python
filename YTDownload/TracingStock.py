import os, sys

import numpy as np
from numpy import *

from collections import OrderedDict
from grs import Stock
from grs import TWSENo

import cPickle as pickle


def readStockdata(filename):
  result_list = []
  
  readobj = open(filename, 'rb')
  content = readobj.read()
  readobj.close()

  rowlist = content.split('\n')
  
  for i,row in enumerate(rowlist):
    if i != 0 and row.strip():
      result_list.append(map(eval, row.split(',')))
  
  return mat(result_list)


def calProb(stockmap):
  buylist=[]
  win_prob = 1.0
  lose_prob = 1.0
  
  for r in stockmap:
    if r[0,3] > 0.85:
      buylist.append(r)
      win_prob = win_prob * r[0,3]
      lose_prob = lose_prob * (1.0 - r[0,3])

  print buylist
  print "Win:",win_prob
  print "Lose:",lose_prob
        
def main():
  stockmap = readStockdata('2017-03-03.txt')
  calProb(stockmap) 

if __name__=="__main__":
  main()

