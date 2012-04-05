=================
django开发经验记录
=================
记录FlexyGears开发过程中收获的django各项问题的解决方案以及心得体会

django开发经验及有用的代码片段
============================

django开发阶段静态文件访问服务的实现方法
-------------------------------------
在使用django进行开发的过程中，需要使用内建的development开发服务器以简化开发流程。由于django开发服务器存在性能问题，因此仅供开发使用。要启用django开发服务器需要在进行相关设置：

setting.py中修改相关目录设置::

	# APP_ROOT_DIR为预先定义好记录了当前文件所在目录信息的变量
	# site_media为开发服务器可以访问到的本地目录名
	MEDIA_ROOT = os.path.join(APP_ROOT_DIR, 'site_media')
	MEDIA_URL = '/site_media/'

url.py中添加访问静态文件的URL配置::

	# 开发服务器中提供的静态文件访问服务。生产环境中需要禁止以避免引起性能问题
	# site_media用于缩短解析规则的代码长度。
	import os
	site_media = os.path.join(os.path.dirname(__file__), '/site_media')
	# 在urlpatterns中添加如下解析规则
	url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),

django开发文件静态文件
-----------------------