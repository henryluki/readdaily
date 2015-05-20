#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson

def index(request):
	return HttpResponse('test')