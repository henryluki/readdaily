# -*- coding=utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
import urllib2,re
import datetime
from lxml import etree
from BeautifulSoup import BeautifulSoup
import cron
from models import RssData 

def page_not_found(request):
    return render_to_response('404.html')

def page_error(request):
    return render_to_response('500.html')

def httpIndex(request):
	return render_to_response('index.html')

def runKeepData(request,param):
	'''
	定时存储
	'''
	c_id=param
	status=cron.cronStart(c_id)
	return render_to_response('404.html',{'status':status})

def readArticle(request,param):
	'''
	阅读文章
	'''
	a_id=param
	arr=RssData().readArticle(a_id)
	article=arr[0]['title']
	return render_to_response('detail.html',{'content':arr,'article':article})

def commonResponse(request,article,template):
	'''
	响应请求
	'''
	article=article
	template=template
	if 'offset' not in request.GET:
		arr=RssData().checkDataCommon(article)
		return render_to_response(template,{'article':article,'content':arr})		
	else:
		offset=request.GET['offset']
		items=RssData().checkDataScroll(article,int(offset))
		return HttpResponse(simplejson.dumps(items,ensure_ascii=False))


'''
 互联网-it资讯
'''
def httpZhihu(request):
	'''
	知乎每日精选
	'''
	# url='http://www.zhihu.com/rss'
	article="知乎每日精选"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpZdaily(request):
	'''
	知乎日报
	'''
	# url='http://www.zhihudaily.net/rss.xml'
	# url='http://hanhanone.vipsinaapp.com/feed/zhihu_dayily'
	article="知乎日报"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def http36kr(request):
	'''
	36kr
	'''
	# url="http://www.36kr.com/feed/"
	article="36氪 | 关注互联网创业"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpGeekpark(request):
	'''
	极客公园
	'''
	# url='http://www.geekpark.net/rss'
	article="极客公园-GeekPark"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpGuokr(request):
	'''
	果壳网
	'''
	# url='http://www.guokr.com/rss/'
	article="果壳网 guokr.com"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear
'''
虎嗅网-虎嗅评论
'''
def httpHuxiu(request):
	'''
	虎嗅网
	'''
	# url='http://www.huxiu.com/rss/1.xml'
	article="虎嗅网"
	template='ajax_b.html'
	answear=commonResponse(request,article,template)
	return answear

'''
豆瓣-小清新论调
'''
def httpDmovie(request):
	'''
	豆瓣影评
	'''
	# url="http://feed.feedsky.com/Doumovie"
	# url="http://www.douban.com/feed/review/movie"
	# temp=parser.httpParser5(url)
	article="豆瓣最受欢迎的影评"
	template='ajax_b.html'
	answear=commonResponse(request,article,template)
	return answear

def httpDbook(request):
	'''
	豆瓣书评
	'''
	# url="http://feed.feedsky.com/Doubook"
	# url="http://www.douban.com/feed/review/book"
	# temp=parser.httpParser5(url)
	article="豆瓣最受欢迎的书评"
	template='ajax_b.html'
	answear=commonResponse(request,article,template)
	return answear

'''
阅读-文学与博览
'''
def httpYige(request):
	'''
	一个
	'''
	# url='http://onehd.herokuapp.com/'
	article="一个-韩寒"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpMeiwen(request):
	'''
	美文日赏
	'''
	# url='http://meiwenrishang.com/rss'
	article="美文日赏"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpYiyan(request):
	article="译言精选-摘要"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpNdweekly(request):
	'''
	南都周刊
	'''
	# url='http://www.nbweekly.com/rss/smw/'
	article="南都周刊"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

'''
摄影-关于艺术与设计
'''
def httpQiyu(request):
	'''
	奇遇网
	'''
	# url='http://www.qiyu.net/rss'
	article="奇遇"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpLetsfilm(request):
	'''
	胶片的味道
	'''
	# url='http://feed.feedsky.com/likeakid'
	# url='http://letsfilm.org/feed'
	article="胶片的味道 | 胶片的味道"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpDcmagcn(request):
	'''
	影像视觉
	'''
	# url='http://www.dcmagcn.com/feed'
	article="影像视觉"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear


def httpImgii(request):
	'''
	IMGII在线视觉杂志
	'''
	# url='http://www.imgii.com/feed'
	article="IMGII在线视觉杂志"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpFotofeel(request):
	'''
	Fotofeel 私摄影
	'''
	# url='http://www.fotofeel.com/rss'
	article="Fotofeel 私摄影 - 情绪·人像·生活"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear
'''
电影-关于电影
'''
def httpCinephi(request):
	'''
	Cinephilia迷影
	'''
	# url='http://cinephilia.net/feed'
	article="Cinephilia迷影"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpSeemovie(request):
	'''
	看电影
	'''
	# url='http://feed.mtime.com/my/seemovie/feed.rss'
	article="看电影·非主流的世界电影之旅"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpYp136(request):
	'''
	电影影评网
	'''
	# url='http://www.yp136.com/feed'
	article="电影影评网"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear
'''
笑话-轻松一刻
'''
def httpQiubai(request):
	'''
	糗事百科
	'''
	# url='http://www.qiushibaike.com/hot/rss'
	article="糗事百科"
	template='ajax_b.html'
	answear=commonResponse(request,article,template)
	return answear



def httpWaduanzi(request):
	'''
	挖段子网
	'''
	# url='http://www.waduanzi.com/feed'
	article="挖段子网"
	template='ajax_b.html'
	answear=commonResponse(request,article,template)
	return answear
'''
生活-关于生活
'''
def httpXinli(request):
	'''
	改变从这里开始 - 壹心理
	'''
	# url='http://feed.xinli001.com/'
	article="改变从这里开始 - 壹心理"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear

def httpJiaren(request):
	'''
	佳人
	'''
	# url='http://jiaren.org/feed/'
	article="佳人"
	template='ajax_a.html'
	answear=commonResponse(request,article,template)
	return answear








	