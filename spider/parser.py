# -*- coding=utf-8 -*-
from django.shortcuts import render_to_response
from models import RssData
from rss.models import Article
import urllib2,re
import datetime
from lxml import etree
from BeautifulSoup import BeautifulSoup
import sys

def httpRequest(url):
	'''
	发送请求
	'''
	try:
		page=None#返回请求内容
		SockFile=None#中间变量
		request=urllib2.Request(url)#使用urllib2模块
		#添加header 模拟客户端
		request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')
		request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		request.add_header('Pragma', 'no-cache')
		opener=urllib2.build_opener()
		SockFile=opener.open(request)
		page=SockFile.read()

	finally:
		if SockFile:
			SockFile.close()

	return page

def httpXpath(text):
	"""keep brief from description and content"""
	root=etree.HTML(text)
	a_brief=root.xpath(u"//p//text()")
	string="<p>"
	reload(sys)
	sys.setdefaultencoding('utf8')
	soup=BeautifulSoup(text)
	b_brief=soup.find('img')
	if b_brief:
		string+=str(b_brief)
		string+="</p><p>"
	for i in range(len(a_brief)):
		if i<2:
			string+=a_brief[i]
	string+=".......</p>"

	return string

'''
代码重用
'''
def httpParser1(url):
	'''
	common:title link description 
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=10:
			num=11-t
			string=httpXpath(descr[num].text)
			newtime=datetime.datetime.strptime(pubDate[num].text[:25],"%a, %d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=descr[num].text
			arr['content']=""

			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)


def httpParser2(url):
	'''
	title link description
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t>=2 and t<=9:
			num=11-t
			string=httpXpath(descr[num].text)
			newtime=datetime.datetime.strptime(pubDate[num].text[:25],"%a, %d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=descr[num].text
			arr['content']=""
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParser3(url):
	'''
	title link description
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t>=2 and t<=9:
			num=11-t
			newtime=datetime.datetime.strptime(pubDate[num].text[:25],"%a, %d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=""
			arr['descr']=descr[num-1].text
			arr['content']=""
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParser4(url):
	'''
    title link description content:encoded
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	soup=BeautifulSoup(content)
	item=soup.findAll('content:encoded')
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=9:
			num=10-t
			string=httpXpath(item[num-1].contents[0].replace('&amp;','&').replace( '&lt;','<').replace('&gt;','>').replace('&quot;','"'))
			newtime=datetime.datetime.strptime(pubDate[num].text[:25],"%a, %d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=descr[num].text
			arr['content']=item[num-1].contents[0].encode('utf-8')
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParser5(url):
	'''
	title link description content:encoded
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	soup=BeautifulSoup(content)
	item=soup.findAll('content:encoded')
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=9:
			num=10-t
			string=httpXpath(item[num-1].contents[0].replace('&amp;','&').replace( '&lt;','<').replace('&gt;','>').replace('&quot;','"'))
			newtime=datetime.datetime.strptime(pubDate[num].text[:25],"%a, %d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=""
			arr['content']=item[num-1].contents[0].encode('utf-8').replace('&amp;','&').replace( '&lt;','<').replace('&gt;','>').replace('&quot;','"')
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParser6(url):
	'''
	title link description content:encoded
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	soup=BeautifulSoup(content)
	item=soup.findAll('content:encoded')
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t>=2 and t<=10:
			num=12-t
			string=httpXpath(item[num-2].contents[2])
			newtime=datetime.datetime.strptime(pubDate[num-2].text[:19],"%Y-%m-%d %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=""
			arr['content']=item[num-2].contents[2].encode('utf-8')
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParser7(url):
	'''
    title link content:encoded
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	soup=BeautifulSoup(content)
	item=soup.findAll('content:encoded')
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=8:
			num=9-t
			string=httpXpath(item[num-1].contents[0])
			newtime=datetime.datetime.strptime(pubDate[num].text[:25],"%a, %d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=""
			arr['content']=item[num-1].contents[0].encode('utf-8')
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParserGuokr(url):
	'''
	果壳：content title id updated
	'''
	content=httpRequest(url)#发送请求
	soup=BeautifulSoup(content)
	item=soup.findAll('content')
	title=soup.findAll('title')
	link=soup.findAll('id')
	pubDate=soup.findAll('updated')
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=10:
			num=11-t
			string=httpXpath(item[num-1].contents[0].replace('&amp;','&').replace( '&lt;','<').replace('&gt;','>').replace('&quot;','"'))
			newtime=datetime.datetime.strptime(pubDate[num].contents[0][:10],"%Y-%m-%d")
			newtime=newtime.strftime('%Y年%m月%d日')
			arr={}
			arr['article']=article
			arr['title']=title[num].contents[0]
			arr['link']=link[num].contents[0]
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=item[num-1].contents[0].encode('utf-8').replace('&amp;','&').replace( '&lt;','<').replace('&gt;','>').replace('&quot;','"')
			arr['content']=""
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParserQiubai(url):
	'''
	糗百：title link description 
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=1:
			num=2-t
			newtime=datetime.datetime.strptime(pubDate[num].text[:24],"%a,%d %b %Y %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=""
			arr['descr']=descr[num].text
			arr['content']=""
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParserNandou(url):
	'''
	南都周刊：title link description 
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//pubDate")
	article=title[0].text
	content=[]
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=10:
			num=11-t
			string=httpXpath(descr[num].text)
			newtime=datetime.datetime.strptime(pubDate[num].text,"%Y/%m/%d %H:%M:%S")
			newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=descr[num].text
			arr['content']=""
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)

def httpParserYige(url):
	'''
	一个：title link description 
	'''
	content=httpRequest(url)#发送请求
	parser=etree.XMLParser(strip_cdata=False)
	root = etree.XML(content,parser)
	descr=root.xpath(u"//description")
	title=root.xpath(u"//title") 
	link=root.xpath(u"//link")
	pubDate=root.xpath(u"//lastBuildDate")
	article=title[0].text
	content=[]
	newtime=datetime.datetime.strptime(pubDate[0].text[:25],"%a, %d %b %Y %H:%M:%S")
	newtime=newtime.strftime('%Y年%m月%d日 %H:%M:%S')
	counter=0
	for t in range(len(title)):
		if t!=0 and t<=3:
			num=4-t
			string=httpXpath(descr[num].text)
			arr={}
			arr['article']=article
			arr['title']=title[num].text
			arr['link']=link[num].text
			arr['pubdate']=newtime
			arr['brief']=string
			arr['descr']=descr[num].text
			arr['content']=""
			if counter==0:
				status=Article.objects.filter(link=link[num].text).exists()
				if not status:
					RssData().keepData(arr)
					counter=1	
			else:
				RssData().keepData(arr)
