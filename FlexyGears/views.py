# coding: utf-8
# FlexyGears默认视图
# Author: Zhang Xiaojing

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from FlexyGears.profiles.models import Profile



'''
FlexyGears默认登录视图
'''
@login_required
def home(request):
	return render_to_response('index.html',
                              RequestContext(request))