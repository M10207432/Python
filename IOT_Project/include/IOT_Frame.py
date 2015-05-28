from socket import socket, AF_INET, SOCK_STREAM
import msvcrt as m
import sys, os
import wx,string
import wx.media
import wx.lib.agw.aquabutton as AB

IP='140.118.172.121'
Port = 12345
wx.Log.SetLogLevel(0)

class IOT_Interface(wx.Frame):
    def __init__(self):
        '''=========================
                Init Parameter
        ========================='''
        self.panel_xsize=1290
        self.panel_ysize=850
        
        self.title_posx=10
        self.title_posy=10
        self.title_sizex=160
        self.title_sizey=100
        self.titleimg="./CustomDraw/Title.png"
        
        self.video_xpos=1000
        self.video_ypos=530
        self.video_xsize=250#560
        self.video_ysize=150#400
        self.videofile='./Video/IOT1.mp4'
        
        self.video2_xpos=1160
        self.video2_ypos=355
        self.video2_xsize=110
        self.video2_ysize=70
        self.videofile2='./Video/IOT2.mp4'

        self.video3_xpos=1010
        self.video3_ypos=420
        self.video3_xsize=90
        self.video3_ysize=60
        self.videofile3='./Video/IOT3.mp4'
        
        self.choose_xpos=700
        self.choose_ypos=450
        self.pre_xpos=100
        self.pre_ypos=550
        self.next_xpos=300
        self.next_ypos=550
        self.buy_xpos=200
        self.buy_ypos=600

        self.rb_offset_x=150
        self.rb_offset_y=-40
        self.evt_xpos1=600
        self.evt_ypos1=305
        self.evt_xpos2=650
        self.evt_ypos2=305
        self.evt_xpos3=751
        self.evt_ypos3=305
        self.inout_xpos1=680
        self.inout_ypos1=375
        self.inout_xpos2=741
        self.inout_ypos2=375
        
        self.imgpos_x=120
        self.imgpos_y=150
        self.imgsize_x=280
        self.imgsize_y=350
        
        self.BGimg='./CustomDraw/BG.png'

        self.listValue=[-1,-1,1,0]
        '''=========================
                Set Up
        ========================='''
        wx.Frame.__init__(self, parent=None, title="IOT Final Project", size=(self.panel_xsize, self.panel_ysize))
        self.panel= MainPanel(self,self.BGimg)
        self.picture=None
        self.connect=False
        self.resurceimg=os.listdir('Resource')
        self.imgindex=0
        
        self.SetBackgroundColour('white')
        
        for i in self.resurceimg:
            print i
        self.Component()                #Create component
        self.ConnectServer(IP, Port)    #Connect to server
        
    def GetParseValue(self,ParserObj):
        panel=self.panel
        self.ParserObj=ParserObj
        #--------------------Label
        
        wx.StaticText(parent=panel, label=self.ParserObj[0], pos=(750,125))
        wx.StaticText(parent=panel, label=self.ParserObj[1], pos=(790,190))

        if self.ParserObj[0]=='Sunny':
            self.listValue[0]=1
        if self.ParserObj[0]=='Rainy':
            self.listValue[0]=0
        if self.ParserObj[0]=='Cloudy':
            self.listValue[0]=0.5

        if self.ParserObj[1]=='Hot':
            self.listValue[1]=1
        if self.ParserObj[1]=='Warm':
            self.listValue[1]=0.5
        if self.ParserObj[1]=='Cold':
            self.listValue[1]=0
            
    def Component(self):
        panel=self.panel

        '''==========================
                BUTTON
        =========================='''
        
        #--------------------Choose your clothes for today
        self.choose_btn=wx.Button(parent=panel, label="Choose your daily wear ><", pos=(self.choose_xpos,self.choose_ypos))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.ChooseFunc, self.choose_btn) #self.Bind(EVT_flag, Function, component)

        #--------------------Buy or Pick
        self.buy_btn=wx.Button(parent=panel, label="Get", pos=(self.buy_xpos,self.buy_ypos))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.BuyFunc, self.buy_btn)

        #--------------------Switch
        self.next_btn=wx.Button(parent=panel, label="Next", pos=(self.next_xpos,self.next_ypos))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.SwitchNext, self.next_btn)
        self.pre_btn=wx.Button(parent=panel, label="Pre", pos=(self.pre_xpos,self.pre_ypos))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.SwitchPre, self.pre_btn)

        #--------------------RadioButton
        self.evt_rb1=wx.RadioButton(parent=panel, label="Date", pos=(self.evt_xpos1+self.rb_offset_x,self.evt_ypos1+self.rb_offset_y), style = wx.RB_GROUP)
        self.evt_rb2=wx.RadioButton(parent=panel, label="Dine together", pos=(self.evt_xpos2+self.rb_offset_x,self.evt_ypos2+self.rb_offset_y))
        self.evt_rb3=wx.RadioButton(parent=panel, label="Tour", pos=(self.evt_xpos3+self.rb_offset_x,self.evt_ypos3+self.rb_offset_y))

        self.Bind(wx.EVT_RADIOBUTTON, self.RadioFun_evt, self.evt_rb1)
        self.Bind(wx.EVT_RADIOBUTTON, self.RadioFun_evt, self.evt_rb2)
        self.Bind(wx.EVT_RADIOBUTTON, self.RadioFun_evt, self.evt_rb3)

        self.inout_rb1=wx.RadioButton(parent=panel, label="Indoor", pos=(self.inout_xpos1+self.rb_offset_x,self.inout_ypos1+self.rb_offset_y), style = wx.RB_GROUP)
        self.inout_rb2=wx.RadioButton(parent=panel, label="Outdoor", pos=(self.inout_xpos2+self.rb_offset_x,self.inout_ypos2+self.rb_offset_y))
        self.Bind(wx.EVT_RADIOBUTTON, self.RadioFun_inout, self.inout_rb1)
        self.Bind(wx.EVT_RADIOBUTTON, self.RadioFun_inout, self.inout_rb2)
        
        #--------------------Media
        
        try:
            self.mc = wx.media.MediaCtrl(parent=panel,
                                         style=wx.SIMPLE_BORDER,
                                         pos=wx.Point(self.video_xpos,self.video_ypos),
                                         size=wx.Size(self.video_xsize,self.video_ysize),
                                         szBackend=wx.media.MEDIABACKEND_WMP10)#pos=wx.Point(100,50),size=wx.Size(320,240)
            self.mc2 = wx.media.MediaCtrl(parent=panel,
                                         style=wx.SIMPLE_BORDER,
                                         pos=wx.Point(self.video2_xpos,self.video2_ypos),
                                         size=wx.Size(self.video2_xsize,self.video2_ysize),
                                         szBackend=wx.media.MEDIABACKEND_WMP10)#pos=wx.Point(100,50),size=wx.Size(320,240)
            self.mc3 = wx.media.MediaCtrl(parent=panel,
                                         style=wx.SIMPLE_BORDER,
                                         pos=wx.Point(self.video3_xpos,self.video3_ypos),
                                         size=wx.Size(self.video3_xsize,self.video3_ysize),
                                         szBackend=wx.media.MEDIABACKEND_WMP10)#pos=wx.Point(100,50),size=wx.Size(320,240)
        except NotImplementedError:
            self.Destroy()
            raise
        
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnPlay)   #trigger OnPlay(), when MEDIA_LOAD

        #------------------Timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)

        self.buy_btn.Disable()
        self.next_btn.Disable()
        self.pre_btn.Disable()
        
        #sizer.Add(self.mc, (1,1), span=(5,1))#, flag=wx.EXPAND)
        
    def ConnectServer(self, ip, port):
        try:
            self.clientsocket=socket(AF_INET, SOCK_STREAM)
            self.clientsocket.connect((IP, port))
            self.clientsocket.settimeout(0.01)
            self.connect=True
            print "Connect Server Done"
        except:
            self.connect=False
            print "Connect Fail"
    
    def ChooseFunc(self, event):
        print "Choose"
        print self.listValue
            
        if self.connect:
            self.clientsocket.send("Choose"+'\r')
            self.clientsocket.send(self.listValue[0]+','+
                                   self.listValue[1]+','+
                                   self.listValue[2]+','+
                                   self.listValue[3]+'\r')
        self.buy_btn.Enable()
        self.next_btn.Enable()
        self.pre_btn.Enable()
        
    def BuyFunc(self, event):
        print "Buy"
        if self.connect:
            self.clientsocket.send("Buy"+'\r')
        
    def SwitchNext(self,event):
        print "Next"
        
        if self.picture:
            self.picture.Destroy()
            
        if self.imgindex >= len(self.resurceimg)-1 :
            self.imgindex=0
        else:
            self.imgindex=self.imgindex+1
        print self.resurceimg[self.imgindex]
        
        self.ShowCloth('Resource/'+self.resurceimg[self.imgindex])
        
    def SwitchPre(self,event):
        print "Pre"
        
        if self.picture:
            self.picture.Destroy()
            
        if self.imgindex == 0 :
            self.imgindex=len(self.resurceimg)-1
        else:
            self.imgindex=self.imgindex-1
        print self.resurceimg[self.imgindex]
        self.ShowCloth('Resource/'+self.resurceimg[self.imgindex])
        
    def ShowCloth(self, imgfile):
        panel=self.panel

        if imgfile.find('png')>0 or imgfile.find('PNG')>0:
            bmp = wx.Image(imgfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        if imgfile.find('jpg')>0 or imgfile.find('JPG')>0:
            bmp = wx.Image(imgfile, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
                
        image = wx.ImageFromBitmap(bmp)
        image = image.Scale(self.imgsize_x, self.imgsize_y, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
    
        self.picture=wx.StaticBitmap(panel, -1, result, (self.imgpos_x, self.imgpos_y), (self.imgsize_x, self.imgsize_y))#(bmp.GetWidth(), bmp.GetHeight())
        
        '''
        gif = wx.Image(opj('bitmaps/image.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        png = wx.Image(opj('bitmaps/image.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        jpg = wx.Image(opj('bitmaps/image.jpg'), wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        '''
        
    def RadioFun_evt(self, event):
        rb_obj=event.GetEventObject()
        print rb_obj.GetLabel()
        
        choose=rb_obj.GetLabel()
        if choose=="Date":
            self.listValue[2]=1
        if choose=="Dine together":
            self.listValue[2]=0.5
        if choose=="Tour":
            self.listValue[2]=0
            
    def RadioFun_inout(self, event):
        rb_obj=event.GetEventObject()
        print rb_obj.GetLabel()
        
        choose=rb_obj.GetLabel()
        if choose=="Indoor":
            self.listValue[3]=0
        if choose=="Outdoor":
            self.listValue[3]=1
            
    def DoLoadFile(self, path):
        print "Load"
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
            
    def OnPlay(self, event):
        print "Play!!!!!!"
        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetVolume(0)
            
        if not self.mc2.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc2.SetVolume(0)

        if not self.mc3.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc3.SetVolume(0)
        
    def OnTimer(self, evt):

        #==============================Video
        offset = self.mc.Tell()
        length=self.mc.Length()
        if offset==0 or offset==-1:
            if not self.mc.Load(self.videofile):
                wx.MessageBox("Unable to load %s: Unsupported format?" % self.videofile,
                              "ERROR",
                              wx.ICON_ERROR | wx.OK)

        offset = self.mc2.Tell()
        length=self.mc2.Length()
        if offset==0 or offset==-1:
            if not self.mc2.Load(self.videofile2):
                wx.MessageBox("Unable to load %s: Unsupported format?" % self.videofile2,
                              "ERROR",
                              wx.ICON_ERROR | wx.OK)

        offset = self.mc3.Tell()
        length=self.mc3.Length()
        if offset==0 or offset==-1:
            if not self.mc3.Load(self.videofile3):
                wx.MessageBox("Unable to load %s: Unsupported format?" % self.videofile3,
                              "ERROR",
                              wx.ICON_ERROR | wx.OK)
                
        #==============================Server Data
        try:
            msg=self.clientsocket.recv(1024)
            if msg:
                print msg
        except:
            pass
        
    def ShutdownDemo(self):

        self.timer.Stop()
        del self.timer
        self.clientsocket.close()

class MainPanel(wx.Panel):
    def __init__(self, parent, BGimg):
        
        self.BGimg=BGimg
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        self.frame = parent
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap(self.BGimg)
        
        dc.DrawBitmap(bmp, 0, 0)
