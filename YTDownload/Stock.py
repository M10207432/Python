import os,sys

import numpy as np
from numpy import *
import matplotlib.pyplot as plt

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

from collections import OrderedDict
from grs import Stock
from grs import TWSENo

from sklearn.neural_network import MLPClassifier
import sklearn as sk

class StockObj():
        def __init__ (self, get_month):
                print "Stock"
                
                self.stockdata=OrderedDict()
                self.today=datetime.now().strftime("%Y/%m/%d")
                self.get_month=get_month
                
                self.OutputData=OrderedDict()
                self.InputData=OrderedDict()
                
        def showStocknum(self):
                twse_no = TWSENo()
                for i in twse_no.all_stock_no:
                        print i,twse_no.searchbyno(i)[i]
                
        def stockGet(self,s_num,month):
                
                stock = Stock(s_num,month)
                time_list=[]
                stock_list=[]
                
                self.stockdata[s_num]=OrderedDict()
                                
                for i in stock.raw:
                        
                        time_obj=re.sub(r"\d+/",str(int(i[0][:i[0].find('/')])+1911)+"/",i[0],1)
                        time=datetime.strptime(time_obj,"%Y/%m/%d")

                        self.stockdata[s_num][time_obj]=i[6]
                        time_list.append(time)
                        stock_list.append(i[6])
                
                #plt.plot(time_list,stock_list)
                #plt.show()
                
                for stock_num in self.stockdata:
                        for  d in self.stockdata[stock_num]:
                                print d,self.stockdata[stock_num][d]
                
        def buyStock(self,s_num,date,count):    #("2330","2016/12/12",3)
                if self.stockdata.has_key(s_num):
                        pay=float(self.stockdata[s_num][date])*count*1000
                        print "You have to pay:",pay
                else:
                        self.stockGet(s_num,3)
                        pay=float(self.stockdata[s_num][date])*count*1000
                        print "You have to pay:",pay
                        
        def cal_BuyorNotbuy(self,s_num,earn,countday):

                if self.InputData.has_key(s_num) == False:
                        self.InputData[s_num]=OrderedDict()
                
                #--------Check Data retrieve & parameter reasonable
                if self.stockdata.has_key(s_num)==False:
                        self.stockGet(s_num,self.get_month)
                while self.stockdata[s_num].has_key(date)==False and date<self.today:
                        t=str(int(date.replace("/",""))+1)
                        date=(t[:4])+"/"+(t[4:6])+"/"+(t[6:8])
                if date>self.today:
                        print "This date is future=>",date
                        return False
                
                d=date  
                while counter<countday:
                        while self.stockdata[s_num].has_key(d)==False and d<self.today:
                                t=str(int(d.replace("/",""))+1)
                                d=(t[:4])+"/"+(t[4:6])+"/"+(t[6:8])
                        if d<self.today:
                                counter+=1
                                #print counter,d
                                
                                t=str(int(d.replace("/",""))+1)
                                d=(t[:4])+"/"+(t[4:6])+"/"+(t[6:8])
                                
                        else:
                                #print "The counterday is too large=%s, limit count is %s" %(countday,counter)
                                return False
                list_key=self.stockdata[s_num].keys() 
                #print "Already Prepare Done, Start Evalaute..."
                #print "Start Date=%s, Stock=%s" % (date,self.stockdata[s_num][date])

                #--------Eval
                for i,date in enumerate(list_key):
                        Earn_Flag==False
                        if i+countday == len(list_key):
                                break
                        
                        for d_index in range(i+1, i+countday+1):
                                diff=float(self.stockdata[s_num][list_key[d_index]])-float(self.stockdata[s_num][date])
                                if diff >= earn:
                                        print "Earn money at %s, value=%s" % (d,self.stockdata[s_num][list_key[d_index]])
                                        Earn_Flag=True
                                        
                        if Earn_Flag == True:
                                self.InputData[s_num][date]=1
                        else:
                                self.InputData[s_num][date]=0
                return self.InputData
                '''
                inc_day=0
                while(len(list_key)-countday > inc_day):
                        counter=0
                        d=date
                        
                        while counter<countday:
                                while self.stockdata[s_num].has_key(d)==False and d<self.today:
                                        t=str(int(d.replace("/",""))+1)
                                        d=(t[:4])+"/"+(t[4:6])+"/"+(t[6:8])
                                        
                                diff=float(self.stockdata[s_num][d])-float(self.stockdata[s_num][date])
                                if diff >= earn:
                                        #print "Earn money at %s, value=%s" % (d,self.stockdata[s_num][d])
                                        Earn_Flag=True
                                counter+=1
                                t=str(int(d.replace("/",""))+1)
                                d=(t[:4])+"/"+(t[4:6])+"/"+(t[6:8]) 
                        if Earn_Flag==False:
                                #print "There is no Earn, so so not buy it"
                                return "Not Buy"
                        else:
                                #print "Earn money"
                                return "Buy"
                '''
        def cal_KDBox(self,s_num,calday):
                print "Evaluate KD value"

                K=50.0
                D=50.0

                if self.OutputData.has_key(s_num) == False:
                        self.OutputData[s_num]=OrderedDict()
                        
                #============Check date
                if self.stockdata.has_key(s_num)==False:
                        self.stockGet(s_num,self.get_month)
                        
                list_key=self.stockdata[s_num].keys()
                if(len(list_key)<calday):
                        print "Calday is too long, list len=%d" % (len(list_key))
                        return False
        
                #============Evalaute KD
                count_day=0
                while(len(list_key)>calday+count_day):
                        max_stock=0
                        min_stock=0xFFFF
                        avg_v=0.0
                        
                        for i in range(calday):
                                v=float(self.stockdata[s_num][list_key[i+count_day]])
                                avg_v = avg_v + v
                                if v>max_stock:
                                        max_stock=v
                                if v<min_stock:
                                        min_stock=v

                        avg_v = avg_v/calday
                        RSV=((self.stockdata[s_num][list_key[calday+count_day]]-min_stock)/(max_stock-min_stock))*100.0
                        now_K=K*(2.0/3.0)+RSV*(1.0/3.0)
                        now_D=D*(2.0/3.0)+now_K*(1.0/3.0)
                        
                        K=now_K
                        D=now_D
                        #print "Date:%s CurStock=%f, RSV=%s, K=%f D=%f (min=%f, max=%f)" % (list_key[calday+count_day],self.stockdata[s_num][list_key[calday+count_day]], RSV, now_K, now_D, min_stock, max_stock),
                        
                        self.InputData[s_num][list_key[calday+count_day]]={    "CurStock" : self.stockdata[s_num][list_key[calday+count_day]],
                                                                               "RSV"      : RSV,
                                                                               "K"        : now_K,
                                                                               "D"        : now_D,
                                                                               "Avg"    : avg_v
                        '''                                         }
                        resultBuyorNot = self.cal_BuyorNotbuy(s_num,list_key[calday+count_day],10,15)                                     
                        if resultBuyorNot == "Buy":
                                #print "Buy"
                                self.OutputData[s_num][list_key[calday+count_day]]=1
                        elif resultBuyorNot == "Not Buy":
                                #print "Not But"
                                self.OutputData[s_num][list_key[calday+count_day]]=0
                        '''
                        count_day=count_day+1
                                                                               
                return self.InputData
                
        def nn_Train(self, inp_para, output):

                for day in Output[Stock_id]:
                        if Input[Stock_id].has_key(day) == True:
                                print day, Input[Stock_id][day], Output[Stock_id][day]

                
                X = np.array([[5,6],[1,2],[3,6],[8,9],[3,1]])
                Y = np.array([30,2,18,72,3])
                test_X = np.array([[11,2],[13,6],[8,9],[3,1]])
                
                mlp = MLPClassifier(    hidden_layer_sizes=(20,), max_iter=100, alpha=1e-4,
                                        solver='lbfgs', verbose=10, tol=1e-6, random_state=1,
                                        learning_rate_init=.1)
                
                mlp.fit(X,Y)
                print mlp.loss_
                for coef in mlp.coefs_:
                        print coef
                print mlp.predict(X)
                     
if __name__=="__main__":
        s=StockObj(get_month = 12)

        
        Stock_id="2330"

        Input = s.cal_BuyorNotbuy(s_num, earn=10, countday=15)
        #Output=s.cal_KDBox(Stock_id,9)
                                                                               
        #s.nn_Train(Input, Output)








