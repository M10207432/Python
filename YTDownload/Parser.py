import pandas,requests
import urllib2

class ParserData():
    def __init__(self,url):
        self.url=url;
    def show(self):
        self.dfs = pandas.read_html(self.url)
        print self.dfs[0]
        
def main():
    print "Parser"
    
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
    
if __name__=="__main__":
    main()
