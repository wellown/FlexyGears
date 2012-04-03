==========================
Django第三方应用开发经验记录
==========================
记录开发FlexyGears过程中使用第三方开发包的经验。以备后续检查使用

django-userena
===============
django-userena\ [#]_\ 是一套django的用户管理开发扩展组件。可以实现的注册、登录、账号激活等完整的用户注册管理功能。而且提供了一套站内的Message功能，功能十分强大。用户注册时可以使用用户的Email地址进行验证。

django-userena的安装
--------------------
django-userena安装可以使用`pip<http://www.pip-installer.org/en/latest/index.html>`_ 进行快速安装，运行下面的指令可以自动完成扩展组件的安装或升级（pip的其他使用方法请参考相关文档）::

	pip install django-userena

django-userena的设置
--------------------
使用django-userena需要在setting.py和urls.py中进行相关的设置


----

.. [#] http://www.django-userena.org/
