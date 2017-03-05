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

'''===========================
        Log Decorate
==========================='''
def showlog(func):
        def d_f(*argv):
                result=func(*argv)
                for i in result:
                        print i
                
                return result
        return d_f

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
                
                #for stock_num in self.stockdata:
                #        for  d in self.stockdata[stock_num]:
                #                print d,self.stockdata[stock_num][d]
                
                
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

                K=50.0
                D=50.0

                if self.InputData.has_key(s_num) == False:
                        self.InputData[s_num]=OrderedDict()
                        
                #============Check date
                if self.stockdata.has_key(s_num)==False:
                        self.stockGet(s_num,self.get_month)
                        
                list_key=self.stockdata[s_num].keys()
                if(len(list_key)<calday):
                        #yield "Calday is too long, list len=%d" % (len(list_key))
                        return False
        
                #============Evalaute KD
                count_day=0
                RSV=0
                ex_RSV=0
                
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
                        
                        if(max_stock!=min_stock):
                                RSV=((self.stockdata[s_num][list_key[calday+count_day]]-min_stock)/(max_stock-min_stock))*100.0
                        else:
                                RSV=ex_RSV
                        ex_RSV=RSV
                        now_K=K*(2.0/3.0)+RSV*(1.0/3.0)
                        now_D=D*(2.0/3.0)+now_K*(1.0/3.0)
                        
                        K=now_K
                        D=now_D

                        #yield "Date:%s CurStock=%f, RSV=%s, K=%f D=%f (min=%f, max=%f)" % (list_key[calday+count_day],self.stockdata[s_num][list_key[calday+count_day]], RSV, now_K, now_D, min_stock, max_stock),

                        if self.InputData[s_num].has_key(list_key[calday+count_day]) == False:
                                self.InputData[s_num][list_key[calday+count_day]] = OrderedDict()
                                
                        self.InputData[s_num][list_key[calday+count_day]]["CurStock"] = self.stockdata[s_num][list_key[calday+count_day]]
                        self.InputData[s_num][list_key[calday+count_day]]["RSV"] = RSV
                        self.InputData[s_num][list_key[calday+count_day]]["K"] = now_K
                        self.InputData[s_num][list_key[calday+count_day]]["D"] = now_D
                        self.InputData[s_num][list_key[calday+count_day]]["Avg"] = avg_v
                        
                        count_day=count_day+1
                                                                               
                return self.InputData
        
        def cal_RSIBox(self, Stock_id, calday):
                if self.InputData.has_key(Stock_id) == False:
                        self.InputData[Stock_id]=OrderedDict()
                        
                #============Check date
                if self.stockdata.has_key(Stock_id) == False:                        
                        self.stockGet(Stock_id,self.get_month)
                        
                list_key = self.stockdata[Stock_id].keys()
                if(len(list_key)<calday):
                        print "Calday is too long, list len=%d" % (len(list_key))
                        return False

                #=================
                count=0
                while(len(list_key)>calday+count):
                        pos_sum = 0
                        pos_per = 0
                        neg_sum = 0
                        neg_per = 0
                        for i in range(calday):
                                val1=self.stockdata[Stock_id][list_key[i+count]]
                                val2=self.stockdata[Stock_id][list_key[i+count+1]]
                                
                                if val2 >= val1:
                                        pos_sum += val2 - val1
                                else:
                                        neg_sum += val1 - val2
                                                                
                        pos_per = float(pos_sum) / float(calday)
                        neg_per = float(neg_sum) / float(calday)
                                                
                        if self.InputData[Stock_id].has_key(list_key[calday+count]) == False:
                                self.InputData[Stock_id][list_key[calday+count]] = OrderedDict()
                        if pos_per!=0 or neg_per!=0:
                                RSI = pos_per/(pos_per + neg_per)
                        else:
                                RSI=0

                        self.InputData[Stock_id][list_key[calday+count]]["Pos_per"]=pos_per
                        self.InputData[Stock_id][list_key[calday+count]]["Neg_per"]=neg_per
                        self.InputData[Stock_id][list_key[calday+count]]["RSI"]=RSI
                        
                        count+=1
                return self.InputData
       
class ClassifyObj():
        
        def __init__ (self, Input, Output):
                print "Classifier"

                self.InputData=Input
                self.OutputData=Output

                self.machine=OrderedDict()

        def nn_Train(self, Stock_id):
                print  "===========Stock %s============" % (Stock_id)
                list_input_data=[]
                list_output_data=[]
			
                for day in self.OutputData[Stock_id]:
                        if self.InputData[Stock_id].has_key(day) == True:

				#Get Input Data
                                tmp_input=[]
                                for k in self.InputData[Stock_id][day]:
                                        tmp_input.append(self.InputData[Stock_id][day][k])
                                list_input_data.append(tmp_input)

				#Get Ontput Data
                                list_output_data.append(self.OutputData[Stock_id][day])
							
				#print day, self.InputData[Stock_id][day], self.OutputData[Stock_id][day]
											
                sample_length=len(list_input_data)
                train_len = sample_length*(2.0/3.0)
                train_len = int(train_len)
						
                Train_X = np.array(list_input_data[:train_len])
                Train_Y = np.array(list_output_data[:train_len])

                Test_X = np.array(list_input_data[train_len:])
                Test_Y = np.array(list_output_data[train_len:])

		#print "Training sample number=%d, Total sample = %d" % (train_len, sample_length)

		#=============================================Learning & Training               
                mlp = MLPClassifier(    hidden_layer_sizes=(20,20), max_iter=100, alpha=1e-4,
									solver='lbfgs', verbose=10, tol=1e-6, random_state=1,
									learning_rate_init=.1)
			
                mlp.fit(Train_X,Train_Y)
			
		#print "MLP Loss=",mlp.loss_

		#print "Buy count=",list_output_data.count(1)
		#print "Not Buy count=",list_output_data.count(0)

                TrainScore = mlp.score(Train_X,Train_Y)
                TestScore = mlp.score(Test_X,Test_Y)
		#print "Score Training=",TrainScore
		#print "Score Test=",TestScore

                self.machine[Stock_id]=OrderedDict()
			
                self.machine[Stock_id]["machine"]=mlp
                self.machine[Stock_id]["TrainScore"]=TrainScore
                self.machine[Stock_id]["TestScore"]=TestScore
                
        def predict(self, Stock_id, day):
                if self.machine.has_key(Stock_id) == False:
                        print "No this machine"
                        return False
		#=============================================Predict                
                predict=[]
                if self.InputData[Stock_id].has_key(day) == True:
                        for k in self.InputData[Stock_id][day]:
                                predict.append(self.InputData[Stock_id][day][k])
                        predict_array=np.array(predict)
                        predict_array=predict_array.reshape(1, -1) # Trasfer to sigle sample pattern
                        print self.machine[Stock_id]["machine"].predict(predict_array)
                        return self.machine[Stock_id]["machine"].predict(predict_array)
                else:
                        print "There is no stock this day %s" % (day)

def main():
	training_month = 12
	predict_date = "2017/03/03"
	RSI_caldate = 9
	KD_caldate = 9

	s=StockObj(get_month = training_month)

	Buy_list=[]
	stock_all_no=[]

	with open("Stock_id.txt",'rb') as stockfile:
		stock_list=stockfile.read().split()
		for i in stock_list:
			if len(i) == 4:
				stock_all_no.append({"id":i})

	#=========================================================Stock Info set (Input/Output)						
	for stock_list in stock_all_no:
			
		Stock_id=stock_list['id']
		print "Get %s Stock Data" % (Stock_id)
		#Input & Output
		s.cal_RSIBox(Stock_id, 9)
		s.cal_KDBox(Stock_id, 9)

		Input = s.InputData	
		Output = s.cal_BuyorNotbuy(Stock_id, earn=10, countday=14)


        #=========================================================Classifier Training       
	classifier_machine = ClassifyObj(s.InputData, s.OutputData)
	for stock_list in stock_all_no:
		Stock_id=stock_list['id']
		#Training
		classifier_machine.nn_Train(Stock_id)

		#Predict for date
		result=classifier_machine.predict(Stock_id, predict_date)
		if result[0] == 1:
			Buy_list.append({"id":Stock_id})

        #=========================================================Show Result
	result_file = open(re.sub("/", "-", predict_date)+".txt",'wb')
	result_file.write(predict_date+'\n')
	for buy_stock in Buy_list:
		print "These can buy"
		print "Stock id %s, Training Score=%f, Testing Score=%f" % (    buy_stock['id'],
                                                                                classifier_machine.machine[buy_stock['id']]["TrainScore"],
                                                                                classifier_machine.machine[buy_stock['id']]["TestScore"])
		result_file.write(buy_stock['id']+',')
		result_file.write(str(s.stockdata[buy_stock['id']][predict_date])+',')
		result_file.write(str(classifier_machine.machine[buy_stock['id']]["TrainScore"])+',')
		result_file.write(str(classifier_machine.machine[buy_stock['id']]["TestScore"])+'\n')
	result_file.close()
        
if __name__=="__main__":
        main()
        


