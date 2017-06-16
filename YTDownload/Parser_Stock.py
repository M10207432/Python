# -*- coding=UTF-8 -*-
import requests
import urllib2
import re
import datetime
import time
from collections import *
import pickle
from threading import Thread
"""========================
0	"日期"
1	"成交股數"
2	"成交金額"
3	"開盤價"
4	"最高價"
5	"最低價"
6	"收盤價"
7	"漲跌價差"
8	"成交筆數"
========================"""

class Stock_Info():
    
    def __init__(self, stock_url, payload):
        self.stock_url = stock_url
        self.payload = payload
        
        self.stockInfo = OrderedDict()
        
    def stockGet(self, stockNo, date):
        self.__checkStockNo__(stockNo);
        
        self.payload["date"] = date
        self.payload["stockNo"] = stockNo
        
        res = requests.get(self.stock_url, self.payload)
        rawdata = res.json()

        if rawdata['stat'] == "OK":
            for info in rawdata['data']:
                self.stockInfo[stockNo].append(info)
            
            return "success"
        else:
            #print rawdata['stat']
            return "fail"
        
    def stockTrace(self, stockNo):
        self.__checkStockNo__(stockNo);
        
        #Local Variable
        request_date = ""
        parse_result = "success"
        cur_date = datetime.datetime.now().strftime("%Y%m%d")
        cur_year = datetime.datetime.now().strftime("%Y")
        cur_month = datetime.datetime.now().strftime("%m")

        #Trace pass year
        for year in range(int(cur_year), 0, -1):
            for month in range(12, 0, -1):
                if month < 10:
                    request_date = str(year) + '0' + str(month) + "01"
                else:
                    request_date = str(year) + str(month) + "01"
                
                if request_date < cur_date:
                    parse_result = self.stockGet(stockNo, request_date) #Trace this date stock
                else:
                    parse_result = "success"
                    
                if parse_result == "fail":
                    break
            if parse_result == "fail":
                print "StockNo %s Done" % (stockNo)
                break
            
    def __checkStockNo__(self, stockNo):
        if self.stockInfo.has_key(stockNo) == False:
            print "Create %s Info" % (stockNo)
            self.stockInfo[stockNo] = []

def StockRefresh():
    Infofile_name = "StockNo_ALL.info"
    Dumpfile_name = "StockInfo"
    stock_url = "http://www.tse.com.tw/exchangeReport/STOCK_DAY"
    payload = {"reponse":"json", "date":"", "stockNo":""}

    thread_q = []
    thread_limit = 10
    
    #Create stock object
    s = Stock_Info(stock_url, payload)

    #Trace all stockNo
    with open(Infofile_name, 'r') as stockNo_ALL:
        for raw_stockNo in stockNo_ALL.readlines():
            stockNo = raw_stockNo.replace("\n",'')
            
            if len(stockNo) == 4:
                #s.stockTrace(stockNo)
                
                thread_q.append(Thread(target = s.stockTrace, name = str(stockNo), args = (stockNo,)))
                thread_q[len(thread_q) - 1].start()

            if len(thread_q) != thread_limit:
                for th_id in range(len(thread_q)):
                    if not thread_q[th_id].is_alive():
                        thread_q.pop(th_id)
                        break
            else:
                while len(thread_q) == thread_limit:
                    for th_id in range(len(thread_q)):
                        if not thread_q[th_id].is_alive():
                            thread_q.pop(th_id)
                            break
                        
    if len(thread_q) > 0:
        for th_id in range(len(thread_q)):
            while (thread_q[th_id].is_alive()):
                pass
            
    #Dump stock info
    pickle.dump(s.stockInfo, open(Dumpfile_name, 'w'))

def main():
    print "Start"
    StockRefresh()
    
if __name__=="__main__":
    main()
