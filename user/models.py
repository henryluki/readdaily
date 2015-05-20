#coding:utf-8
from django.db import models,connection
from django.contrib.auth.models import User

class profile(models.Model):
	weibo_id=models.CharField(max_length=50)
	name=models.CharField(max_length=50)
	description=models.CharField(max_length=256)
	avatar=models.URLField()
	created_at=models.CharField(max_length=50)

class collections(models.Model):
	article_id=models.IntegerField()
	collected_at=models.CharField(max_length=50)
	user_id=models.IntegerField()
	
class profile_manager(object):
	"""docstring for profile_manager"""
	def __init__(self):
		super(profile_manager, self).__init__()
		self.table = profile

	def save(self,profile):
		user_ins=self.table(weibo_id=profile['weibo_id'],name=profile['name'],description=profile['description'],avatar=profile['avatar'],created_at=profile['created_at'])
		user_ins.save()

	def check_or_save(self,profile):
		user_ins=self.table
		status=user_ins.objects.filter(weibo_id=profile['weibo_id']).exists()
		if not status:
			self.save(profile)
			return "save success!"
		else:
			isname=user_ins.objects.filter(name=profile['name']).exists()
			if not isname:
				user_ins.ins.objects.filter(weibo_id=profile['weibo_id']).update(name=profile['name'])
			else:
				return user_ins.objects.filter(weibo_id=profile['weibo_id']).values('id')

		
class collections_manager(object):
	"""docstring for collections_manager"""
	def __init__(self):
		super(collections_manager, self).__init__()
		self.table=collections
	
	def save(self,collections):
		coll_ins=self.table
		status=coll_ins.objects.filter(article_id=collections['article_id']).exists()
		if not status:
			coll_ins=self.table(article_id=collections['article_id'],collected_at=collections['collected_at'],user_id=collections['user_id'])
			coll_ins.save()

	def profile_check(self,name):
		user_ins=profile
		user=user_ins.objects.filter(name=name).values('avatar','description')[0]
		coll_ins=self.table
		articles=coll_ins.objects.raw("""
			SELECT r.id,r.title,r.brief,c.id AS coll_id,c.collected_at FROM rss_article r INNER JOIN user_collections c ON r.id=c.article_id INNER JOIN user_profile p ON c.user_id=p.id WHERE p.name=%s ORDER BY c.id DESC LIMIT 10
			""",[name])
		return (user,articles)

	def user_check(self,name):
		coll_ins=self.table
		articles=coll_ins.objects.raw("""
			SELECT r.id,r.title,r.brief,c.id AS coll_id,c.collected_at FROM rss_article r INNER JOIN user_collections c ON r.id=c.article_id INNER JOIN auth_user p ON c.user_id=p.id WHERE p.username=%s ORDER BY c.id DESC LIMIT 10
			""",[name])
		return articles

	def profile_check_json(self,name,offset):
		coll_ins=self.table
		offset=5+5*offset
		data=coll_ins.objects.raw("""
			SELECT r.id,r.title,r.brief,c.id AS coll_id,c.collected_at FROM rss_article r INNER JOIN user_collections c ON r.id=c.article_id INNER JOIN user_profile p ON c.user_id=p.id WHERE p.name=%s ORDER BY c.id DESC LIMIT %s,5
			""",[name,offset])
		articles=[]
		for d in data:
			arr={
			'id':d.id,
			'title':d.title,
			'brief':d.brief,
			'coll_id':d.coll_id
			}
			articles.append(arr)
		return articles

	def user_check_json(self,name,offset):
		coll_ins=self.table
		offset=5+5*offset
		data=coll_ins.objects.raw("""
			SELECT r.id,r.title,r.brief,c.id AS coll_id,c.collected_at FROM rss_article r INNER JOIN user_collections c ON r.id=c.article_id INNER JOIN auth_user p ON c.user_id=p.id WHERE p.username=%s ORDER BY c.id DESC LIMIT %s,5
			""",[name,offset])
		articles=[]
		for d in data:
			arr={
			'id':d.id,
			'title':d.title,
			'brief':d.brief,
			'coll_id':d.coll_id
			}
			articles.append(arr)
		return articles

	def delete(self,coll_id):
		coll_ins=self.table
		coll_ins.objects.filter(id=coll_id).delete()

	def test(self):
		coll_ins=self.table
		time=coll_ins.objects.all().values('collected_at')[0:5]
		return time





