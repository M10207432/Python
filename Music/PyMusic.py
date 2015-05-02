import wx,string
from wx.lib.filebrowsebutton import FileBrowseButton
import os

class MySalger(wx.Frame):
    def __init__(self,parent,title):
        super(MySalger, self).__init__(parent, title=title, size=(500,100))

        p=wx.Panel(self)
        
        self.fbb=FileBrowseButton(p, labelText="Select file:", fileMask="*.WAV")
        btn=wx.Button(p, -1, "Play")
        self.Bind(wx.EVT_BUTTON, self.OnPlaySound, btn)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.fbb, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL)
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(sizer, 0, wx.EXPAND|wx.ALL, 15)
        p.SetSizer(border)
        
        self.Show()
        
    def OnPlaySound(self, event):
        filename=self.fbb.GetValue()
        self.sound=wx.Sound(filename)
        if self.sound.IsOk():
            print "OK"
            self.sound.Play(wx.SOUND_ASYNC)
        else:
            print "Not Ok"
            wx.MessageBox("Invalid sound file", "Error")
        
        
    def CreateMenu(self):
        menubar = wx.MenuBar()
        fileMenu= wx.Menu()

        fitem= fileMenu.Append(wx.NewId(), '&Open', 'Open a File')
        menubar.Append(fileMenu, '&File')
        
        self.SetMenuBar(menubar)
    
        self.Bind(wx.EVT_MENU, self.onBrowse, fitem) #Bind the EVT method
    

    def OnQuit(self, e):
        self.Close()
    
if __name__=="__main__":
    print "Music !!"
    app = wx.App()
    frame = MySalger(None, title='Hi')
    app.MainLoop()
