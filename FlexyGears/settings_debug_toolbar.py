# coding: utf-8
# filename: django-debug-toolbar.py
# Project:  FlexyGears
# Author:   Zhangxiaojing(wellown@gmail.com)

from django.conf import settings

# 安装debug_toolbar程序
INSTALLED_APPS += (
    'debug_toolbar',
)

# 设置debug_toolbar模板目录
TEMPLATE_DIRS += (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'd:/pve/Lib/site-packages/debug_toolbar/templates',
)

# 设置中间件
MIDDLEWARE_CLASSES += (
    # 启用django-debug-toolbar中间件
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# debug_toolbar需要的设置
INTERNAL_IPS = ('127.0.0.1',)

