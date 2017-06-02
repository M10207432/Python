import pandas,requests
import urllib2
import re
from Download import *
from Stock import *
from PIL import Image


def Instagram(url):
    img=[]
    res=requests.get(url)
    m = re.compile(r"display_src\":\ \"(.*?).jpg")

    for i in m.findall(res.text):
        img.append(i+".jpg")

    if len(img)==1:
        res=urllib2.urlopen(img[0])
        with open("img.jpg","wb") as f:
            for rawdata in res.read():
                f.write(rawdata)
    else:
        print "Amount of Img is wrong!!!"

    #=====================================
    for i in range(3):
        I=Image.open("img.jpg")
        I.show()
def main():
    print "Parser"
    
    #DL_URL=""
    #D=VideoDL("video2.mp4",DL_URL)
    #s=StockObj()
    #s.showStocknum()
    Instagram("")
    

if __name__=="__main__":
    main()
