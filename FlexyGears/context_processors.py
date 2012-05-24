# coding: utf-8
# project: FlexyGears
# Author: Zhang Xiaojing

from django.contrib.auth.models import User
from FlexyGears.profiles.models import Profile

def global_vars( request ):
	"""
		获取用户的个性化设置信息。并添加到各模板的Context中，供模板访问使用
	"""
	try:
		profile = Profile.objects.get( user_id=request.user.id )
	except:
		return { 'profile': '',}
	return {
		#'request': request,
		'profile': profile,
		}
