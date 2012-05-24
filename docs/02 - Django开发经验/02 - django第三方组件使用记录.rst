==============================
Django第三方应用开发经验记录
==============================
记录开发FlexyGears过程中使用第三方开发包的经验。以备后续检查使用

django-userena
===============
django-userena\ [#]_\ 是一套django的用户管理开发扩展组件。可以实现的注册、登录、账号激活等完整的用户注册管理功能。而且提供了一套站内的Message功能，功能十分强大。用户注册时可以使用用户的Email地址进行验证。

django-userena的安装
--------------------
django-userena安装可以使用 `pip <http://www.pip-installer.org/en/latest/index.html>`_  进行快速安装，运行下面的指令可以自动完成扩展组件的安装或升级（pip的其他使用方法请参考相关文档）::

	pip install django-userena

django-userena的设置
--------------------
使用django-userena需要在setting.py和urls.py中进行相关的设置。setting.py中需要增加的设置如下（在默认配置下）::

	INSTALLED_APPS = (
	    # 用户注册功能所需要的应用
    	'userena',
    	'guardian',
    	'easy_thumbnails',
    	# 由于userena仅提供abstract profile定义，因此使用userena必须自定义UserProfile
    	'FlexyGears.profiles',
	)
	# userena所需要的设置
	AUTH_PROFILE_MODULE = 'profiles.Profile'
	# Email后端应用供userena使用。
	Email_BACKEND = 'django.core.mail.backends.dummy.Email_Backend'
	# userena backends settings
	AUTHENTICATION_BACKENDS = (
	    'userena.backends.UserenaAuthenticationBackend',
	    'guardian.backends.ObjectPermissionBackend',
	    'django.contrib.auth.backends.ModelBackend',
	)
	# userena登录相关设置
	LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
	LOGIN_URL = '/accounts/signin/'
	LOGOUT_URL = '/accounts/signout/'
	
	# userena在用户注册后不需要执行激活操作(默认为True)
	USERENA_ACTIVATION_REQUIRED = False
	USERENA_DISABLE_PROFILE_LIST = True
	USERENA_MUGSHOT_SIZE = 140

	# Django-guardian所需要的设置
	ANONYMOUS_USER_ID = -1

url.py中需要增加用户管理相关URL解析规则如下::
	
	(r'^accounts/', include('userena.urls')),

django-userena中的组件easy-thumbnails所需的扩展库PIL
---------------------------------------------------
easy-thumbnails是django的用于处理图像生成缩略图的扩展组件。该组件的运行，需要python环境安装PIL（ `Python Image Library <http://www.pythonware.com/products/pil/>`_ ）。在64位Win7操作系统环境下，使用64位python可能会遇到“无法找到python，无法安装PIL库”的问题。要解决这个问题：

* 直接安装64位的PIL扩展库。由于官方网站提供的是32位的Windows安装版本，所以需要找64位版本。在 `LDF <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_ 可以找到。

对于使用Linux等系统的还可以：

* 直接从源代码安装。可以从官方网站下载 PIL-1.1.7.tar.gz，使用pip安装。（这种安装方式需要本地编译器）

自定义django-userena中的用户登录Form
----------------------------------
使用userena的过程中，难免会遇到对原有Form进行调整的需求。可以采用继承的方式对userena中的Form进行修改甚至重写。

为了使用自定义的Form，需要在url.py中，在调用对应view的时候修改默认Form参数。例如::

	url(r'^accounts/signin/$', 'userena.views.signin',
      {'auth_form': SigninFormExtra}, name='userena_signin'),

上述代码即修改了原有登录时所使用的Form，将从原有的SigninForm改成了项目自定义的SigninFormExtra。

有关userena的各个视图所调用的Form，可以参考userena的开发手册\ [#]_\ 。


django-debug-toolbar
====================
django-debug-toolbar\ [#]_\ 是django开发过程中的非常有用的调试工具。在开发项目中安装加载之后，可以随时查看页面调用过程中的 HTTP头、Request、相关SQL语句等内容。对django开发过程中的调试提供了非常有力的支持。django-debug-toolbar需要依赖django 1.1 及的以上版本。

django-debug-toolbar的安装
--------------------------
使用PIP可以实现快速安装::
	
	pip install django-debug-toolbar

django-debug-toolbar在开发项目中启用
-----------------------------------
要在开发项目中启用django-debug-toolbar，可以按照以下步骤执行::

	1. 将django-debug-toolbar安装后的目录加入Python Path.（通常使用PIP安装后，该目录就已经设置好了。
	如果遇到Import Error之类的错误可以检查一下这个设置）

	2. 修改setting.py，在项目中启用该功能：

		# 加载中间件
		MIDDLEWARE_CLASSES = (
		    # 启用django-debug-toolbar中间件，
		    # 注意：中间件加载顺序可能会对debug-toolbar的行为发生影响
		    # 注意：在本中间件加载前的其他中间件活动，debug-toolbar不再跟踪
		    'debug_toolbar.middleware.DebugToolbarMiddleware',
		)

		# 安装应用
		INSTALLED_APPS = (
		    # 跟在其他已安装的APP之后。对顺序不敏感
		    'debug_toolbar',
		)

		# 定义生效的IP地址
		INTERNAL_IPS = ('127.0.0.1',)

		# 定义debug-toolbar的模板目录
		TEMPLATE_DIRS = (
		    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
		    # Always use forward slashes, even on Windows.
		    # Don't forget to use absolute paths, not relative paths.
		    os.path.join(APP_ROOT_DIR, 'templates/'),
		    'path/to/debug_toolbar/templates'
		)

	3. django-debug-toolbar应该已经可以开始工作了。 



	

----

.. [#] django-userena官方网站：http://www.django-userena.org/
.. [#] django-userena开发手册：http://docs.django-userena.org/en/latest/index.html
.. [#] django-debug-toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar
