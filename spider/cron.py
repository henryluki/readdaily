#coding:utf-8
import parser

def cronStart(c_id):

	c_id=int(c_id)
	if c_id ==1:
		#6小时
		urls=[]
		urls.append('http://hanhanone.vipsinaapp.com/feed/zhihu_dayily')
		urls.append('http://www.zhihu.com/rss')
		urls.append('http://www.waduanzi.com/feed')
		urls.append('http://www.36kr.com/feed/')
		urls.append('http://yikerss.miantiao.me/rss')
		map(parser.httpParser1,urls)
		
		# parser.httpParser3('http://www.huxiu.com/rss/4.xml')
		# urls1=[]
		# urls1.append('http://www.huxiu.com/rss/1.xml')
		# urls1.append('http://www.huxiu.com/rss/4.xml')
		# urls1.append('http://www.huxiu.com/rss/6.xml')
		# for url in urls:
		# 	parser.httpParser1(url)

	elif c_id ==2:
		#24小时
		parser.httpParser1('http://feed.xinli001.com/')
		parser.httpParserQiubai('http://www.qiushibaike.com/hot/rss')
		parser.httpParserYige('http://onehd.herokuapp.com/')
		parser.httpParserMeiwen('http://meiwenrishang.com/rss')
		parser.httpParser7('http://www.pingwest.com/feed/')
		parser.httpParser6('http://www.geekpark.net/rss')
		
	elif c_id==3:
		#2 days
		# parser.httpParser7('http://letsfilm.org/feed')
		parser.httpParserGuokr('http://www.guokr.com/rss/')
		parser.httpParser5('http://jiaren.org/feed/')
		# parser.httpParser5('http://feed.feedsky.com/yeeyan-select')
	
	elif c_id ==4:
		#3天
		parser.httpParser7('http://www.yp136.com/feed')
		parser.httpParser2('http://www.fotofeel.com/rss')
		parser.httpParser4('http://cinephilia.net/feed')
		# urls=[]
		# urls.append('http://www.douban.com/feed/review/movie')
		# urls.append('http://www.douban.com/feed/review/book')
		# urls.append('http://cinephilia.net/feed')
		# for url in urls:
			# parser.httpParser4(url)
			
	elif c_id ==5:
		#7天
		# parser.httpParser1('http://feed.mtime.com/my/seemovie/feed.rss')
		# parser.httpParser2('http://www.qiyu.net/rss')
		urls=[]
		urls.append('http://www.dcmagcn.com/feed')
		urls.append('http://www.imgii.com/feed')
		map(parser.httpParser7,url)


	elif c_id==6:
		#especial
		parser.httpParser7('http://letsfilm.org/feed')

	elif c_id==7:
		#test
		pass

