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
    res=requests.get(URL)
    page=re.search('"og:image" content="(.*?)"',res.text)
    Maxpage=re.search('openimg\((.*?)\)',res.text).group(1).split(',')[1]
    print Maxpage[1:len(Maxpage)-1]
    print page.group(1)
def main():
    
    YYLS(URL)
if __name__=="__main__":
    main()
