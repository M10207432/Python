import sys, os
import wx,string

os.sys.path.append("./include")
import IOT_Frame as MainFrame
import IOT_Parse as MainParse

def main():
    '''=========================
            Parse
        {Sunny, Rainy, Cloudy}
        {Hot, Warm, Cold}
    ========================='''
    ParserObj=MainParse.WebParse()
    #ParserObj.ParseWeather()
    #data=ParserObj.ParseConstellation(2)#0~11
    
    ParserObj=['Rainy','Cold']
    
    '''=========================
        Interface & Connect
    ========================='''
    app = wx.App()
    frame = MainFrame.IOT_Interface()
    frame.GetParseValue(ParserObj)
    frame.Show()
    app.MainLoop()
    
    
if __name__=="__main__":
    main()
