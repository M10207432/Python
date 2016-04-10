import requests
import re
import json
import urlparse

import shutil

JP_Proxy={"http_proxy":"http://103.56.218.194",
          "https_proxy":"https://103.56.218.194",
          "ftp_proxy":"ftp://103.56.218.194"}

URL="http://8yyls.com/116304/"

def YouTube(URL):
    res=requests.get(URL,proxies=(JP_Proxy))    
    m=re.search('"args":({.*?}),',res.text)
    print m.groups()
    j=json.loads(m.group(1))
    
    p=urlparse.parse_qs(j["url_encoded_fmt_stream_map"])
    print p['url'][0]

    res2=requests.get(p['url'][0],stream=True) 
        
    f=open('a.mp4','wb')
    shutil.copyfileobj(res2.raw,f)
    f.close()
    
def YYLS(URL):
    #-------------------------Get Maxpage and url
    res=requests.get(URL)
    page=re.search('"og:image" content="(.*?)"',res.text)
    Maxpage=re.search('openimg\((.*?)\)',res.text).group(1).split(',')[1]
    '''
    print Maxpage[1:len(Maxpage)-1]
    print page.group(1)
    '''
    #-------------------------Save all img  url
    p=int(Maxpage[1:len(Maxpage)-1])
    imgurl_list=[]
    url_page=page.group(1)[:page.group(1).find('.jpg')-3]
    for i in range(1,int(Maxpage[1:len(Maxpage)-1])+1):
        p="00"+str(i)
        while len(p)>3:
            p=p[1:]
        imgurl_list.append(url_page+p+".jpg")
    '''
    for i in imgurl_list:
        print i
    '''     
    #-------------------------Save img
    img_name=1
    for imgurl in imgurl_list:        
        res2=requests.get(imgurl,stream=True)
        f=open(str(img_name)+'.jpg','wb')
        shutil.copyfileobj(res2.raw,f)
        f.close()

        img_name+=1
    
def main():
    
    YYLS(URL)
if __name__=="__main__":
    main()
