#coding:utf-8
from django.db import models,connection

class Scroll(models.Manager):
	def article(self,article,offset):
		article=article
		offset=offset
		cursor=connection.cursor()
		cursor.execute("""
			SELECT id,title,link,pubdate,brief,descr,content FROM rss_article WHERE article=%s ORDER BY pubdate DESC LIMIT %s,5
			""",[article,offset])
		fetchall=cursor.fetchall()
		data=[]
		for obj in fetchall:
			arr={}
			arr['id']=obj[0]
			arr['title']=obj[1]
			arr['link']=obj[2]
			arr['pubdate']=obj[3]
			arr['brief']=obj[4]
			arr['descr']=obj[5]
			arr['content']=obj[6]
			data.append(arr)
		return data

class Article_Scroll(models.Model):
	#自定义sql语句
	article=models.CharField(max_length=50)
	title=models.CharField(max_length=256)
	link=models.CharField(max_length=256)
	pubdate=models.CharField(max_length=50)
	brief=models.TextField()
	descr=models.TextField()
	content=models.TextField()
	objects=Scroll()

class Article(models.Model):
	article=models.CharField(max_length=50)
	title=models.CharField(max_length=256)
	link=models.CharField(max_length=256)
	pubdate=models.CharField(max_length=50)
	brief=models.TextField()
	descr=models.TextField()
	content=models.TextField()