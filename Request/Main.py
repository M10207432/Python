import requests
import re
import json
import urlparse

import shutil

JP_Proxy={"http":"http://43.255.106.64:3128"}
URL="https://www.youtube.com/watch?v=fIQ4VoLHAEg"

def main():
    res=requests.get(URL,proxies=(JP_Proxy))
    m=re.search('"args":({.*?}),',res.text)
    j=json.loads(m.group(1))
    p=urlparse.parse_qs(j["url_encoded_fmt_stream_map"])
    print p['url'][0]

    res2=requests.get(p['url'][0],stream=True)
    
        
    f=open('a.mp4','wb')
    shutil.copyfileobj(res2.raw,f)
    f.close()
    

if __name__=="__main__":
    main()
