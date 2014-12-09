#coding:utf-8
from rss.models import Article,Article_Scroll
from lxml import etree
import datetime

class RssData:
	""" keep data to mysql """

	def __init__(self):
		pass

	def keepData(self,arr):
		article=arr['article']
		pubdate=arr['pubdate']
		title=arr['title']
		link=arr['link']
		brief=arr['brief']
		descr=arr['descr']
		content=arr['content']
		a1=Article(article=article,title=title,link=link,pubdate=pubdate,brief=brief,descr=descr,content=content)
		a1.save()

	def checkData(self,article,offset):
		article=article
		offset=offset
		if offset==0:
			arr=RssData().checkDataCommon(article)
		else:
			arr=RssData().checkDataScroll(article,offset)
		return arr

	def checkDataScroll(self,article,offset):
		article=article
		if article=="一个-韩寒" or article=="糗事百科":
			offset=3+5*offset
			arr=Article_Scroll.objects.article(article,offset)
		else:
			offset=10+5*offset
			arr=Article_Scroll.objects.article(article,offset)
		return arr

	def checkDataCommon(self,article):
		article=article
		if article=="一个-韩寒" or article=="糗事百科":
			arr=Article.objects.filter(article=article).order_by("-pubdate")[0:3]
		else:
			arr=Article.objects.filter(article=article).order_by("-pubdate")[0:10]
		return arr


	def readArticle(self,a_id):
		a_id=int(a_id)
		arr=Article.objects.filter(id=a_id).values()
		return arr
