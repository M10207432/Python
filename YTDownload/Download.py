import os,sys
import requests
import re
import json

class YTDownloader():
	def __init__(self,url):
		print "Boot"
		self.url=url
	def download(self):
		print "Download"
		res=requests.get(self.url)		
		#print res.text
		self.request_g=re.search('"args":({.*?}),',res.text)
		#print self.request_g.group(0)
		#print self.request_g.group(1)
		self.jd=json.loads(self.request_g.group(1))
		for key,v in self.jd.item():
			print key
			
class VideoDL():
    def __init__(self,filename,url):
        print "Download"
        self.url=url
        self.filename=filename;

        self.getResponse()
        
    def getResponse(self):
        self.rawdata=requests.get(self.url)
        
        #====================Line TV====================
        #print self.rawdata.content
        #self.LineTV_DL()

        #====================AKSvideo====================
        self.AKSvideo_DL()

        #====================Twtch Download====================
        #self.Twtch_DL()
        
    def AKSvideo_DL(self):
        str_pat=re.compile(r'html5player.setVideoHLS\(\'(.*?)\'\)')
        result=str_pat.findall(self.rawdata.text)
        self.r_text=result[0].replace('hls.m3u8','hls-360p0.ts')
        
        
        print "AKSVideo Download..."
        video=open(self.filename,'wb')
        counter=0
        fail_counter=0
        
        while fail_counter<3:
            self.r_text=self.r_text.replace("hls-360p"+str(counter-1),"hls-360p"+str(counter))
            print "Process"+str(counter)+"..."
            counter+=1
            
            source=requests.get(self.r_text)
            if source.text.find("404")<0:
                for i in source:
                    video.write(i)
                fail_counter=0
            else:
                fail_counter+=1
                pass
        video.close()
        
    def LineTV_DL(self):
        print "Line TV Download..."
        p={"__gda__":"1486564281_34434dc4d7b3ed5f8fd6c12825153247"}
        h={ 'Host': 'tv-line.pstatic.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept': "*/*",
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://tv.line.me/v/1302313/list/104143',
            'Origin': 'https://tv.line.me',
            'Connection': 'keep-alive'}
        h1={'Host': 'ad-cpv.line.me',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://tv.line.me/v/1302313/list/104143',
            'Origin':'https://tv.line.me',
            'Connection': 'keep-alive'}

        self.rawdata=requests.get(self.url)
        print self.rawdata.text

    def Twtch_DL(self):
        print "Twitch"
        self.rawdata=requests.get(self.url)
        print self.rawdata.text
        
