import os,sys
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from datetime import datetime
import re

from grs import Stock
from grs import TWSENo

def test():
	dataset=[[1,6],[8,6]]
	dataMat=mat(dataset).T
	plt.scatter(dataMat[0],dataMat[1],c='red',marker='o')	
	
	X=np.linspace(-2,2,100)
	Y=2.8*X+9
	
	plt.plot(X,Y)
	plt.show()
	
def stockGet():
	
	stock = Stock('2330',3)
	time_list=[]
	stock_list=[]
	
	print len(stock.raw)                 
	for i in stock.raw:
		
		time_obj=re.sub(r"\d+/",str(int(i[0][:i[0].find('/')])+1911)+"/",i[0],1)
		time=datetime.strptime(time_obj,"%Y/%m/%d")

		#print time,i[6]
		time_list.append(time)
		stock_list.append(i[6])

	plt.plot(time_list,stock_list)
	plt.show()
	'''
	twse_no=TWSENo()
	for n in twse_no.all_stock_name:
		print n
	'''
