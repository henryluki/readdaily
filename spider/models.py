#coding:utf-8
from rss.models import Article,Article_Scroll
from lxml import etree
import datetime

class RssData:

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
		# a1, created = Article.objects.get_or_create(article=article,title=title,link=link,pubdate=pubdate,brief=brief,descr=descr,content=content)

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

	def countNum(self):
		num=Article.objects.count()
		return num

	def indexPage(self):
		#取出 互联网 笑话 生活 阅读 摄影 电影 最新的一条
		arr=[]
		plist=["36氪","豆瓣一刻","知乎日报","挖段子网","改变从这里开始 - 壹心理","胶片的味道 | 胶片的味道","Cinephilia迷影"]
		for i in range(len(plist)):
			arr.append(Article.objects.filter(article=plist[i]).order_by("-pubdate")[0:1])
		return arr




