from socket import socket, AF_INET, SOCK_STREAM
import msvcrt as m
import flask
import flask.views
from flask import request

import sys, os

os.sys.path.append("./include")
import IOT_Frame as MainFrame
import IOT_Parse as MainParse

IP='localhost'
port = 8000

    
def Client_SendData(data):
    s= socket(AF_INET, SOCK_STREAM)
    s.connect((IP, port))
    s.settimeout(0.1)

    #RECV -> SEND
    msg=s.recv(1024)
    s.send(data)
          
def main():
    '''
    #Client_SendData(str(1)+'\n')
    
    MainFrame.Hello()
    
    ParserObj=MainParse.WebParse()
    ParserObj.ParseWeather()
    #data=ParserObj.ParseConstellation(2)#0~11
    '''
    
if __name__=="__main__":
    main()
