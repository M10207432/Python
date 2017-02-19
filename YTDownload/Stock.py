import os,sys

import numpy as np
from numpy import *
import matplotlib.pyplot as plt

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

from grs import Stock
from grs import TWSENo

class StockObj():
        def __init__ (self):
                print "Stock"
                
        def showStocknum(self):
                twse_no = TWSENo()
                for i in twse_no.all_stock_no:
                        print i,twse_no.searchbyno(i)[i]
                
        def stockGet(self,num):
                
                stock = Stock(num,3)
                time_list=[]
                stock_list=[]
                
                print len(stock.raw)                 
                for i in stock.raw:
                        
                        time_obj=re.sub(r"\d+/",str(int(i[0][:i[0].find('/')])+1911)+"/",i[0],1)
                        time=datetime.strptime(time_obj,"%Y/%m/%d")
                        time_list.append(time)
                        stock_list.append(i[6])

                plt.plot(time_list,stock_list)
                plt.show()
if __name__=="__main__":
        s=StockObj()
        s.showStocknum()  
