import urllib2
from xml.dom import minidom
from lxml import etree
import HTMLParser
from lxml.html import fromstring, tostring

class WebParse():
    def __init__(self):
        print "Web Parse Begin"
        self.weatherweb='http://opendata.cwb.gov.tw/opendata/MFC/F-C0032-001.xml'
        self.Constellationweb='http://astro.click108.com.tw/'
        
    def ParseWeather(self):
        print "ParseWeather Parse Begin"
        
        w_web=urllib2.urlopen(self.weatherweb)
        xmldoc = minidom.parse(w_web)
        root = xmldoc.documentElement

        node = root.getElementsByTagName('location')
        for i in range(len(node)):
            itemname=node[i].getElementsByTagName('locationName')
            itempara=node[i].getElementsByTagName('parameterName')
            itemtime=node[i].getElementsByTagName('startTime')
            print "================================================="

            name = itemname[0].toxml()
            w_status = itempara[0].toxml()
            T = itempara[3].toxml()
            time = itemtime[0].toxml()
            
            print name, w_status, T
            print time
            
    def ParseConstellation(self,num):
        print "ParseConstellation Parse Begin"
        '''======================================================
                            First Choose Constellation
        ======================================================'''
        webdata=urllib2.urlopen(self.Constellationweb)
        textcode=HTMLParser.HTMLParser()

        webHTMLdata=webdata.read()
        ET=etree.HTML(webHTMLdata)

        #0~11 Constellation <no tbody>
        tr=ET.xpath('body/div/div/table/tr/td/div/div/div/div/div/ul/li')[num]
        
        v=etree.tostring(tr)
        v=textcode.unescape(v)
        web=v[v.find('<a href=')+9:v.find(' style=')-1]
        C_name=v[v.find(' title=')+8:v.find('>',v.find(' title='))-1]
        
        print C_name
        #print web

        '''======================================================
                            Final Parse information
        ======================================================'''
        webdata=urllib2.urlopen(web)
        textcode=HTMLParser.HTMLParser()

        webHTMLdata=webdata.read()
        ET=etree.HTML(webHTMLdata)
        
        #0->Luck num, 1->Lucky color, 2->Lucky site, 3->Lucky time
        tr=ET.xpath('body/div/table/tr/td/div/div/div/div/div/h4')[1]

        v=etree.tostring(tr)
        v=textcode.unescape(v)
        print v
        return v    
        
    
