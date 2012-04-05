# coding: utf-8
# FlexyGears默认视图
# Author: Zhang Xiaojing

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


'''
FlexyGears默认登录视图
'''
@login_required
def home(request):
    return render_to_response('index.html',
                              RequestContext(request))