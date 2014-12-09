#coding:utf-8
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
handler404 = 'spider.views.page_not_found'
handler500 = 'spider.views.page_error'

urlpatterns = patterns('',
   
    #首页
    url(r'^$','spider.views.httpIndex',name='httpIndex'),
    #看文章
    url(r'article/(\d+)/$','spider.views.readArticle',name='readArticle'),
    #定时存数据
    url(r'keepData/(\d+)/$','spider.views.runKeepData',name='runKeepData'),
    #互联网
    url(r'zhihu/$','spider.views.httpZhihu',name='httpZhihu'),
    url(r'36kr/$','spider.views.http36kr',name='http36kr'),
    url(r'huxiu/$','spider.views.httpHuxiu',name='httpHuxiu'),
    url(r'geekpark/$','spider.views.httpGeekpark',name='httpGeekpark'),
    url(r'zdaily/$','spider.views.httpZdaily',name='httpZdaily'),
    url(r'guokr/$','spider.views.httpGuokr',name='httpGuokr'),
    #豆瓣
    url(r'Dmovie/$','spider.views.httpDmovie',name='httpDmovie'),
    url(r'Dbook/$','spider.views.httpDbook',name='httpDbook'),
    #阅读
    url(r'yige/$','spider.views.httpYige',name='httpYige'),
    url(r'meiwen/$','spider.views.httpMeiwen',name='httpMeiwen'),
    url(r'ndweekly/$','spider.views.httpNdweekly',name='httpNdweekly'),
    #摄影
    url(r'qiyu/$','spider.views.httpQiyu',name='httpQiyu'),
    url(r'letsfilm/$','spider.views.httpLetsfilm',name='httpLetsfilm'),
    url(r'dcmagcn/$','spider.views.httpDcmagcn',name='httpDcmagcn'),
    url(r'imgii/$','spider.views.httpImgii',name='httpImgii'),
    url(r'fotofeel/$','spider.views.httpFotofeel',name='httpFotofeel'),
    # 电影
    url(r'cinephi/$','spider.views.httpCinephi',name='httpCinephi'),
    url(r'seemovie/$','spider.views.httpSeemovie',name='httpSeemovie'),
    url(r'yp136/$','spider.views.httpYp136',name='httpYp136'),
    #笑话
    url(r'qiubai/$','spider.views.httpQiubai',name='httpQiubai'),
    url(r'waduanzi/$','spider.views.httpWaduanzi',name='httpWaduanzi'),
    #生活
    url(r'xinli/$','spider.views.httpXinli',name='httpXinli'),
    url(r'jiaren/$','spider.views.httpJiaren',name='httpJiaren'),
    url(r'yiyan/$','spider.views.httpYiyan',name='httpYiyan'),
    
    # url(r'^$', 'spider.views.home', name='home'),
    # url(r'^spider/', include('spider.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
