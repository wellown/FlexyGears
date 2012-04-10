# coding: utf-8
# project: FlexyGears
# Author: Zhang Xiaojing

from django.contrib.auth.models import User
from FlexyGears.profiles.models import Profile

def global_vars( request ):
	"""
		获取用户的个性化设置信息。
	if request.path == 'account/signout'
		return
	"""
	try:
		profile = Profile.objects.get( user_id=request.user.id )
	except:
		return { 'profile': '',}
	return {
		#'request': request,
		'profile': profile,
		}
