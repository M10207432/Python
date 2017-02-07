import pandas,requests
import urllib2
import re

class ParserData():
    def __init__(self,url):
        self.url=url;
    def show(self):
        self.dfs = pandas.read_html(self.url)
        print self.dfs[0]
        
class VideoDL():
    def __init__(self,url):
        print "Download"
        self.url=url

        self.getResponse()
        
    def getResponse(self):
        self.rawdata=requests.get(self.url)
        
        #====================Line TV====================
        self.AKSvideo_DL()

        #====================AKSvideo====================
        self.AKSvideo_DL()
        
    def AKSvideo_DL(self):
        str_pat=re.compile(r'html5player.setVideoHLS\(\'(.*?)\'\)')
        result=str_pat.findall(self.rawdata.text)
        self.r_text=result[0].replace('hls.m3u8','hls-360p0.ts')
        self.AKSvideo_DL()
        
        print "AKSVideo Download..."
        video=open("video.mp4",'wb')
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


        
def main():
    print "Parser"
    DL_URL=""
    D=VideoDL(DL_URL)
    
    '''
    url="https://tv-line.pstatic.net/global/read/TVCAST_2016_12_12_4/531C05F3830FF32C24335E6793894013F83_muploader_f_1080P_1920_5120_192-000001.ts?__gda__=1486400602_db42852b53a2a5a9012f56e1f8d32298"
    web1=requests.get(url)
    
    with open("1.mp4",'wb') as f:
        for i in web1:
            f.write(i)
            
    url="https://tv-line.pstatic.net/global/read/TVCAST_2016_12_12_4/531C05F3830FF32C24335E6793894013F83_muploader_f_1080P_1920_5120_192-000002.ts?__gda__=1486400602_db42852b53a2a5a9012f56e1f8d32298"
    web2=requests.get(url)
    
    with open("2.mp4",'wb') as f:
        for i in web2:
            f.write(i)
    with open("total.mp4",'wb') as f:
        for i in web1:
            f.write(i)
        for i in web2:
            f.write(i)
    '''
if __name__=="__main__":
    main()
