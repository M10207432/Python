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

                self.machine=OrderedDict()

        def showStocknum(self):
                stock_all=[]
                        
                twse_no = TWSENo()
                for i in twse_no.all_stock_no:
                        tmp_dict={}
                        tmp_dict["id"]=i
                        tmp_dict["name"]=twse_no.searchbyno(i)[i]
                        stock_all.append(tmp_dict)
                        #print i,twse_no.searchbyno(i)[i]
                        
                return stock_all
        
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
                '''
                for stock_num in self.stockdata:
                        for  d in self.stockdata[stock_num]:
                                print d,self.stockdata[stock_num][d]
                '''
        def buyStock(self,s_num,date,count):    #("2330","2016/12/12",3)
                if self.stockdata.has_key(s_num):
                        pay=float(self.stockdata[s_num][date])*count*1000
                        print "You have to pay:",pay
                else:
                        self.stockGet(s_num,3)
                        pay=float(self.stockdata[s_num][date])*count*1000
                        print "You have to pay:",pay
                        
        def cal_BuyorNotbuy(self,s_num,earn,countday):

                if self.OutputData.has_key(s_num) == False:
                        self.OutputData[s_num]=OrderedDict()
                        
                #--------Check Data retrieve & parameter reasonable
                if self.stockdata.has_key(s_num)==False:
                        self.stockGet(s_num,self.get_month)                
                
                list_key=self.stockdata[s_num].keys()
                
                #--------Eval
                for i,date in enumerate(list_key):
                        Earn_Flag=False
                        if i+countday == len(list_key):
                                break
                        
                        for d_index in range(i+1, i+countday+1):
                                diff=float(self.stockdata[s_num][list_key[d_index]])-float(self.stockdata[s_num][date])
                                if diff >= earn:
                                        #print "Earn money at %s, value=%s" % (list_key[d_index], self.stockdata[s_num][list_key[d_index]])
                                        Earn_Flag=True
                                        
                        if Earn_Flag == True:
                                self.OutputData[s_num][date]=1
                        else:
                                self.OutputData[s_num][date]=0

                return self.OutputData
                
        def cal_KDBox(self,s_num,calday):
                print "Evaluate KD value"

                K=50.0
                D=50.0

                if self.InputData.has_key(s_num) == False:
                        self.InputData[s_num]=OrderedDict()
                        
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
                        self.InputData[s_num][list_key[calday+count_day]] = OrderedDict()
                        self.InputData[s_num][list_key[calday+count_day]]={    "CurStock" : self.stockdata[s_num][list_key[calday+count_day]],
                                                                               "RSV"      : RSV,
                                                                               "K"        : now_K,
                                                                               "D"        : now_D,
                                                                               "Avg"    : avg_v   }
                        count_day=count_day+1
                                                                               
                return self.InputData
                
        def nn_Train(self, Stock_id, Input, Output):
                print "===========Stock %s============" % (Stock_id)
                list_input_data=[]
                list_output_data=[]
                
                for day in Output[Stock_id]:
                        if Input[Stock_id].has_key(day) == True:

                                #Get Input Data
                                tmp_input=[]
                                for k in Input[Stock_id][day]:
                                        tmp_input.append(Input[Stock_id][day][k])
                                list_input_data.append(tmp_input)

                                #Get Ontput Data
                                list_output_data.append(Output[Stock_id][day])
                                
                                #print day, Input[Stock_id][day], Output[Stock_id][day]
                                                
                sample_length=len(list_input_data)
                train_len = sample_length*(2.0/3.0)
                train_len = int(train_len)
                                
                Train_X = np.array(list_input_data[:train_len])
                Train_Y = np.array(list_output_data[:train_len])

                Test_X = np.array(list_input_data[train_len:])
                Test_Y = np.array(list_output_data[train_len:])

                print "Training sample number=%d, Total sample = %d" % (train_len, sample_length)

                #=============================================Learning & Training
                X = np.array([[5,6],[1,2],[3,6],[8,9],[3,1]])
                Y = np.array([30,2,18,72,3])
                test_X = np.array([[11,2],[13,6],[8,9],[3,1]])
                
                mlp = MLPClassifier(    hidden_layer_sizes=(20,), max_iter=100, alpha=1e-4,
                                        solver='lbfgs', verbose=10, tol=1e-6, random_state=1,
                                        learning_rate_init=.1)
                
                mlp.fit(Train_X,Train_Y)
                
                print "MLP Loss=",mlp.loss_

                print "Buy count=",list_output_data.count(1)
                print "Not Buy count=",list_output_data.count(0)

                TrainScore = mlp.score(Train_X,Train_Y)
                TestScore = mlp.score(Test_X,Test_Y)
                print "Score Training=",TrainScore
                print "Score Test=",TestScore

                self.machine[Stock_id]=OrderedDict()
                
                self.machine[Stock_id]["machine"]=mlp
                self.machine[Stock_id]["TrainScore"]=TrainScore
                self.machine[Stock_id]["TestScore"]=TestScore
                
        def predict(self, s_num, day):
                if self.machine.has_key(s_num) == False:
                        print "No this machine"
                        return False
                #=============================================Predict                
                predict=[]
                if self.InputData[s_num].has_key(day) == True:
                        for k in self.InputData[s_num][day]:
                                predict.append(Input[s_num][day][k])
                        predict_array=np.array(predict)
                        predict_array=predict_array.reshape(1, -1) # Trasfer to sigle sample pattern
                        print self.machine[s_num]["machine"].predict(predict_array)
                        return self.machine[s_num]["machine"].predict(predict_array)
                else:
                        print "There is no stock this day %s" % (day)
                
if __name__=="__main__":
        
        s=StockObj(get_month = 36)

        Buy_list=[]
        stock_all_no=s.showStocknum()
        
        for stock_list in stock_all_no:
                if len(stock_list['id'])!=4:
                        continue
                
                Stock_id=stock_list['id']
                
                Input = s.cal_KDBox(Stock_id,9)
                Output = s.cal_BuyorNotbuy(Stock_id, earn=10, countday=14)
                                                                                       
                s.nn_Train(Stock_id, Input, Output)
                result=s.predict(Stock_id, "2017/02/23")
                if result[0] == 1:
                        Buy_list.append({"id":Stock_id})

        for buy_stock in Buy_list:
                print "These can buy"
                print "Stock id %s, Training Score=%f, Testing Score=%f" % (buy_stock['id'],
                                                                          s.machine[buy_stock['id']]["TrainScore"],
                                                                          s.machine[buy_stock['id']]["TestScore"])
                
        







