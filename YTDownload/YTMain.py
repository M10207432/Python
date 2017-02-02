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

def main():
	print "YTDownloder"
	Machine=YTDownloader("https://www.youtube.com/watch?v=XpYMag46-sU")
	Machine.download()
if __name__=="__main__":
	main()
