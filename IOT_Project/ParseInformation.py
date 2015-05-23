from socket import socket, AF_INET, SOCK_STREAM
import msvcrt as m
import sys, os
import wx,string
import wx.media
os.sys.path.append("./include")
import IOT_Frame as MainFrame
import IOT_Parse as MainParse

IP='localhost'
Port = 8000
 
def Client_SendData(data):
    s= socket(AF_INET, SOCK_STREAM)
    s.connect((IP, port))
    s.settimeout(0.1)

    #RECV -> SEND
    msg=s.recv(1024)
    s.send(data)
    
class MySalgar(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="Hi", size=(500,300))
        self.panel=wx.Panel(self)
        self.picture=None
        self.connect=False
        self.resurceimg=os.listdir('Resource')
        self.imgindex=0
        
        for i in self.resurceimg:
            print i
        self.Component()                #Create component
        self.ConnectServer(IP, Port)    #Connect to server
        
    def Component(self):
        panel=self.panel

        '''==========================
            TEST & TEXTCTRL
        =========================='''
        wx.StaticText(parent = panel, label="1", pos=(10, 10))
        self.a=wx.TextCtrl(parent = panel, pos=(100,10))
        
        wx.StaticText(parent = panel, pos=(10, 10))
        self.b=wx.TextCtrl(parent = panel, pos=(100,50))

        '''==========================
                BUTTON
        =========================='''
        #--------------------Choose your clothes for today
        self.choose_btn=wx.Button(parent=panel, label="Choose your daily wear ><", pos=(10,150))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.ChooseFunc, self.choose_btn) #self.Bind(EVT_flag, Function, component)

        #--------------------Buy or Pick
        self.buy_btn=wx.Button(parent=panel, label="Buy", pos=(80,100))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.BuyFunc, self.buy_btn)

        #--------------------Switch
        self.next_btn=wx.Button(parent=panel, label="Next", pos=(10,200))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.SwitchNext, self.next_btn)
        self.pre_btn=wx.Button(parent=panel, label="Pre", pos=(100,200))#size=(size_x, size_y)
        self.Bind(wx.EVT_BUTTON, self.SwitchPre, self.pre_btn)
        
    def ConnectServer(self, ip, port):
        try:
            self.clientsocket=socket(AF_INET, SOCK_STREAM)
            self.clientsocket.connect((IP, port))
            self.clientsocket.settimeout(0.1)
            self.connect=True
            print "Connect Server Done"
        except:
            self.connect=False
            print "Connect Fail"
    
    def ChooseFunc(self, event):
        print "Choose"
        if self.connect:
            self.clientsocket.send("Choose")

    def BuyFunc(self, event):
        print "Buy"
        if self.connect:
            self.clientsocket.send("Buy")

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
        
        size_x=200
        size_y=250

        if imgfile.find('png')>0 or imgfile.find('PNG')>0:
            bmp = wx.Image(imgfile, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        if imgfile.find('jpg')>0 or imgfile.find('JPG')>0:
            bmp = wx.Image(imgfile, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
                
        image = wx.ImageFromBitmap(bmp)
        image = image.Scale(size_x, size_y, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
    
        self.picture=wx.StaticBitmap(panel, -1, result, (250, 5), (size_x, size_y))#(bmp.GetWidth(), bmp.GetHeight())
        
        '''
        gif = wx.Image(opj('bitmaps/image.gif'), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        png = wx.Image(opj('bitmaps/image.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        jpg = wx.Image(opj('bitmaps/image.jpg'), wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        '''
        
class StaticText(wx.StaticText):
    """
    A StaticText that only updates the label if it has changed, to
    help reduce potential flicker since these controls would be
    updated very frequently otherwise.
    """
    def SetLabel(self, label):

        if label <> self.GetLabel():
            wx.StaticText.SetLabel(self, label)

#----------------------------------------------------------------------

class TestPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1,
                          style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)

        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER,
                                         #szBackend=wx.media.MEDIABACKEND_DIRECTSHOW
                                         #szBackend=wx.media.MEDIABACKEND_QUICKTIME
                                         #szBackend=wx.media.MEDIABACKEND_WMP10
                                         )

        except NotImplementedError:
            self.Destroy()
            raise

        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)

        btn1 = wx.Button(self, -1, "Load File")
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, btn1)

        btn2 = wx.Button(self, -1, "Play")
        self.Bind(wx.EVT_BUTTON, self.OnPlay, btn2)
        self.playBtn = btn2

        btn3 = wx.Button(self, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.OnPause, btn3)

        btn4 = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.OnStop, btn4)

        slider = slider = wx.Slider(self, -1, 0,0.0001,3000, pos=(120,680), style = wx.SL_HORIZONTAL | wx.SL_LABELS, size = (400, -1))
        self.slider = slider
        slider.SetMinSize((150, -1))
        self.Bind(wx.EVT_SLIDER, self.OnSeek, slider)

        self.st_size = StaticText(self, -1, size=(100,-1))
        self.st_len  = StaticText(self, -1, size=(100,-1))
        self.st_pos  = StaticText(self, -1, size=(100,-1))

        # setup the layout
        sizer = wx.GridBagSizer(5,5)
        sizer.Add(self.mc, (1,1), span=(5,1))#, flag=wx.EXPAND)
        sizer.Add(btn1, (1,3))
        sizer.Add(btn2, (2,3))
        sizer.Add(btn3, (3,3))
        sizer.Add(btn4, (4,3))
        sizer.Add(slider, (6,1), flag=wx.EXPAND)
        sizer.Add(self.st_size, (1, 5))
        sizer.Add(self.st_len,  (2, 5))
        sizer.Add(self.st_pos,  (3, 5))
        self.SetSizer(sizer)

        #wx.CallAfter(self.DoLoadFile, os.path.abspath("1.mp4"))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)


    def OnLoadFile(self, evt):

        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.DoLoadFile(path)

        dlg.Destroy()


    def DoLoadFile(self, path):

        #self.playBtn.Disable()

        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize()
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())


    def OnMediaLoaded(self, evt):

        self.playBtn.Enable()


    def OnPlay(self, evt):

        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize()
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())


    def OnPause(self, evt):

        self.mc.Pause()


    def OnStop(self, evt):

        self.mc.Stop()


    def OnSeek(self, evt):

        offset = self.slider.GetValue()
        self.mc.Seek(offset)

    def OnTimer(self, evt):

        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s' % self.mc.GetBestSize())
        self.st_len.SetLabel('length: %d seconds' % (self.mc.Length()/1000))
        self.st_pos.SetLabel('position: %d' % offset)


    def ShutdownDemo(self):

        self.timer.Stop()
        del self.timer
        
def main():
    '''
    app = wx.App()
    frame = MySalgar()
    frame.Show()
    app.MainLoop()
    '''
    
    app = wx.App(0)

    frame = wx.Frame(None)
    panel = TestPanel(frame)
    frame.Show()

    app.MainLoop()
    '''
    #Client_SendData(str(1)+'\n')
    
    MainFrame.Hello()
    
    ParserObj=MainParse.WebParse()
    ParserObj.ParseWeather()
    #data=ParserObj.ParseConstellation(2)#0~11
    '''
    
if __name__=="__main__":
    main()
