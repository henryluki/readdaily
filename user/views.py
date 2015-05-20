# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from weibo import APIClient
from models import profile_manager,collections_manager
import datetime

APP_KEY = 'app key' # app key
APP_SECRET = 'app secret' # app secret
CALLBACK_URL = 'http://readdaily.sinaapp.com/login_check/' # callback url

#weibo login
def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url
 
def weibo_login(request): 
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    auth_url = client.get_authorize_url()
   
    return HttpResponseRedirect(auth_url)


def weibo_login_check(request):
    code = request.GET.get('code', None)
    back_to_url = _get_referer_url(request)
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token 
    expires_in = r.expires_in
    
    request.session['oauth_access_token'] = r
    client.set_access_token(access_token, expires_in)
    uid=client.account.get_uid.get()  
    data=client.users.show.get(uid=uid['uid'])
    user={
    'weibo_id':data['id'],
    'name':data['screen_name'],
    'description':data['description'],
    'avatar':data['avatar_large'],
    'created_at':datetime.datetime.now().strftime('%y年%m月%d日 %H:%M:%S'),
    }

    #check the database
    user_ins=profile_manager()
    user_ins.check_or_save(user)
    request.session['user']=user
    return HttpResponseRedirect(back_to_url)
 
def weibo_logout(request):
    if request.session.get('oauth_access_token'):
        del request.session['oauth_access_token']
    del request.session['user']
    back_to_url = _get_referer_url(request)
    return HttpResponseRedirect(back_to_url)

#auth
def auth_signin(request):
    if not request.POST:
        return HttpResponse(simplejson.dumps({'code':403}))
    username=request.POST['lusername']
    password=request.POST['lpassword']
    status=User.objects.filter(username=username).exists()
    if not status:
        return HttpResponse(simplejson.dumps({'exist':'a'}))
    user = authenticate(username=username, password=password)
    if not user:
        return HttpResponse(simplejson.dumps({'exist':'b'}))
    else:
        user={
        'name':username,
        'description':"的个人收藏",
        'avatar':'/static/img/neat.jpg'
        }
        request.session['user']=user
        return HttpResponse(simplejson.dumps({'username':username,'avatar':'/static/img/neat.jpg'}))
        


def auth_signout(request):
    pass

def auth_signup(request):
    if not request.POST:
        return HttpResponse(simplejson.dumps({'code':403}))
    rusername=request.POST['rusername']
    remail=request.POST['remail']
    rpassword=request.POST['rpassword']

    u_status=User.objects.filter(username=rusername).exists()
    if u_status:
        return HttpResponse(simplejson.dumps({'exist':'a'}))
    e_status=User.objects.filter(email=remail).exists()
    if e_status:
        return HttpResponse(simplejson.dumps({'exist':'b'}))

    user=User.objects.create_user(rusername,remail,rpassword)
    user.save()
    return HttpResponse(simplejson.dumps({'code':200}))


#user
def user_weibo_page(request,param):
    name=param
    user_me=request.session.get('user')
    coll_ins=collections_manager()
    if 'offset' not in request.GET:
        user,articles=coll_ins.profile_check(name)
        user['name']=name
        title=name+u' 的个人收藏'
        return render_to_response('collections.html',{'user_me':user_me,'article':title,'user':user,'articles':articles})
    else:
        offset=request.GET['offset']
        articles=coll_ins.profile_check_json(name,int(offset))
        return HttpResponse(simplejson.dumps(articles,ensure_ascii=False))

def user_common_page(request,param):
    username=param
    user_me=request.session.get('user')
    coll_ins=collections_manager()
    if 'offset' not in request.GET:
        articles=coll_ins.user_check(username)
        user={
            'name':username,
            'description':"的个人收藏",
            'avatar':'/static/img/neat.jpg'
            }
        title=username+u' 的个人收藏'
        return render_to_response('collections.html',{'user_me':user_me,'article':title,'user':user,'articles':articles})
    else:
        offset=request.GET['offset']
        articles=coll_ins.user_check_json(username,int(offset))
        return HttpResponse(simplejson.dumps(articles,ensure_ascii=False))

def user_weibo_collect(request,param):
    user=request.session.get('user')
    if not user:
        HttpResponseRedirect('/login/')
    user_ins=profile_manager()
    user_id=user_ins.check_or_save(user)[0]['id']
    article_id=param
    collections={
    'article_id':article_id,
    'collected_at':datetime.datetime.now().strftime('%y年%m月%d日 %H:%M:%S'),
    'user_id':user_id
    }
    coll_ins=collections_manager()
    coll_ins.save(collections)
    return HttpResponse(simplejson.dumps({'code':200}))

def user_common_collect(request,param):
    user=request.session.get('user')
    if not user:
        HttpResponseRedirect('/login/')
    user_id=User.objects.filter(username=user['name']).values('id')[0]['id']
    article_id=param
    collections={
    'article_id':article_id,
    'collected_at':datetime.datetime.now().strftime('%y年%m月%d日 %H:%M:%S'),
    'user_id':user_id
    }
    coll_ins=collections_manager()
    coll_ins.save(collections)
    return HttpResponse(simplejson.dumps({'code':200}))

def user_remove(request):
    coll_id=request.POST['coll_id']
    if not coll_id:      
        code=500
    else:
        code=200
        coll_ins=collections_manager()
        coll_ins.delete(int(coll_id))
    return HttpResponse(simplejson.dumps({'code':code}))

def user_setting(request):
    return render_to_response('')


def user_test(request):
    coll_ins=collections_manager()
    time=coll_ins.test()
    return render_to_response('test.html',{'data':time})

