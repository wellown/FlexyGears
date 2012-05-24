=================
django开发经验记录
=================
记录FlexyGears开发过程中收获的django各项问题的解决方案以及心得体会

django开发经验及有用的代码片段
============================

django开发阶段静态文件访问服务的实现方法
----------------------------------------
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

django中的TEMPLATE_CONTEXT_PROCESSORS
--------------------------------------
在使用django开发过程中，有时会遇到一些需要在不同模板中访问整站共用的信息的时候。如果依赖对应的View在逐个构建，那么代码会非常繁琐和冗余。为了解决这个问题，通过查看django中request对象中user成员对象的构建方式，发现可以使用TEMPLATE_CONTEXT_PROCESSORS设置来解决。

django中的TEMPLATE_CONTEXT_PROCESSORS \ [#]_\  可以对Context进行修改，加入（或修改）指定的共用变量。以便在模板中使用。为了在整站的所有模板中都可以方便的显示用户Profile中的相关设定，因此，需要在RequestContext中增加Profile对象。具体的代码如下::

	#setting.py中设置TEMPLATE_CONTEXT_PROCESSORS
	TEMPLATE_CONTEXT_PROCESSORS = (
	    'django.contrib.auth.context_processors.auth',
	    'django.core.context_processors.i18n',
	    'django.core.context_processors.media',
	    # 将用户的个人设置加入到默认变量中，供全站使用
	    'FlexyGears.context_processors.global_vars',
	)

	# 编写代码实现添加功能
	# context_processors.py
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



django国际化开发经验
-----------------------
django提供了较好的国际化开发手段——使用GNU的gettext就能够实现多语言的实现了。在实际的使用过程中，由于对django的翻译文件（po/mo）加载机制不了解，因此在开发过程中还是出现了不少问题。并且看起来短时间是无法解决了。这些问题是：

# 当django提供的扩展库国际化不完全的时候，需要修改扩展库中的po文件，会打破项目文件组织结构。po文件难于维护
	* 由于中文目前在国际开源项目中的参与度不足，很多扩展库都存在中文翻译不完全的情况。因此，在某个项目中使用开源提供的扩展库常常需要对po文件进行定制翻译
	* 安装到系统中的扩展库通常在系统环境中。如果将定制翻译的po文件放置到系统目录中，则该文件会脱离项目文件结构。且在安装到其他环境中时遇到权限问题（由于需要操作Python系统目录）
	* 直接将定义开发的文件放在项目（project）目录结构中，并且符合django的i18n目录要求，则在开发过程中更新po文件时可能出现“覆盖错误”——部分扩展库运行所需要的字符串被删除了。
# 将扩展库源代码树直接复制到项目文件夹中需要保持一定的目录结构，无法与项目开发文件做明显的区分
	* 将需要修改的扩展库放在项目文件夹中显然也是一个获得相应代码修改权限的方案。但这样做有明显的以下几个缺点：
		+ 为保持扩展库的访问方式不变，需要直接放在项目根目录中。这样扩展库与项目开发代码容易混淆在一起。特别是多人开发环境中可能会出现修改了错误的代码而引入Bug
		+ 当扩展库需要升级时，需要特别小心，否则可能导致部分开发代码在升级过程中丢失而导致项目运行错误
		+ 仅由于需要修改扩展库的极少量的代码，而将整个扩展库引入到源代码管理系统中，显然不够“敏捷”
# 扩展库或APP中包含Locale文件夹，将可能扰乱项目中po、mo文件的加载规则，导致加载错误，特别是一个View中的翻译资源需要从多个地方加载的时候。
	* 在项目的多个APP中使用独立的Locale文件，有关po、mo文件的加载规则还需要进一步研究

当前FlexyGears开发项目中国际化开发解决方案
*****************************************
为了规避上述问题，在FlexyGears开发过程中采取以下方案：
# Locale文件集中存放在Project目录中（settings.py所在文件目录）
# 使用django-admin.py生成po文件时使用如下指令::

	django-admin.py makemessages.py -l zh-cn.fg

# 手工编辑po文件，将各个APP中的po文件整合在一起，存放在Locale目录中。对于中文的存放目录应该是::

	<FlexyGears>/locale/zh_CN/LC_MESSAGES

# 使用django-admin.py编译生成mo文件::

	django-admin.py compilemessages

# 需要加入代码管理器管理的文件夹包括：
	* zh-cn.fg
	* zh-cn.userena

django-admin生成po文件遇到xgettext错误的解决方案
***********************************************
在Windows环境中，使用django-admin.py生成po文件时可能会遇到xgettext错误。实际上是由于django-admin.py脚本无法找到GNU gettext程序导致的（该程序在Linux环境中天生具备）。要解决该错误，需要从GNU安装gettext程序。从 `GUN服务器 <http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/>`_ 下载两个文件gettext-runtime-X.zip 和 gettext-tools-X.zip X为版本号
	
	注意版本低了会报错“Django internationalization requires GNU gettext 0.15 or newer”）

下载后放在解压在一个目录里，然后把下面的bin目录加到你系统路径中就可以正常使用django-admin.py生成po文件了。

使用msgmerge合并po文件
**********************
在GNU的gettext程序包中，提供了对po文件进行操作的多种命令行程序。其中msgmerge可以帮助完成两个po文件的合并工作。这对于降低翻译文件的合并工作量很有好处。

django代码学习
==============
这里记录使用django开发过程中，对现有django代码的学习成果

使用url匹配规则名称隔离模板与源代码
----------------------------------
在django-userena的template中使用视图名称实现模板与代码之间的隔离。是一个非常好的最佳实践。看下面的代码::

	# 在模板中
	<ul class="nav nav-list">
        <li class="nav-header">个人信息面板</li>
        <li {%block profile-sidebar-detail%}{%endblock%}><a href="{% url userena_profile_detail user.username %}">{% trans "View profile" %} &raquo;</a></li>
        <li {%block profile-sidebar-edit%}{%endblock%}><a href="{% url userena_profile_edit user.username %}">{% trans "Edit details" %} &raquo;</a></li>
        <li {%block profile-sidebar-password%}{%endblock%}><a href="{% url userena_password_change user.username %}">{% trans "Change password" %} &raquo;</a></li>
        <li {%block profile-sidebar-email%}{%endblock%}><a href="{% url userena_email_change user.username %}">{% trans "Change email" %} &raquo;</a></li>
    </ul>

查看上述代码，我发现了一个有意思的标记{% url %}。django文档中对于这个标记的说明\ [#]_\ 如下：

	Returns an absolute path reference (a URL without the domain name) matching a given view function and optional parameters. This is a way to output links without violating the DRY principle by having to hard-code URLs in your templates

从文档中，我看到url tag是返回指定View的URL地址。指定view的方法是：path.to.some_view。而在userena代码中并没有这样写，它使用了更加易于理解的方法，如：userena_profile_detail。那么这个名字是如何找到的呢？秘密就在url.py中。请看下面的代码::

	# Edit profile
    url(r'^(?P<username>[\.\w]+)/edit/$',
       userena_views.profile_edit,
       name='userena_profile_edit'),

从代码中可以看到，在设计url分拣规则是，给指定的view设定了名字。（上例中的代码设定的名字是“userena_profile_edit”）。

这样设定的好处很明显：将源代码的组织与模板隔离了开来。当需要进行源代码包重构时，仅需要修改url匹配规则文件即可。模板就不需要修改了。


----
.. [#] https://docs.djangoproject.com/en/1.4/ref/templates/api/#playing-with-context-objects
.. [#] https://docs.djangoproject.com/en/dev/ref/templates/builtins/#url