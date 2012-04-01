========
VirtuENV
========

VirtualENV是什么？
=================
virtualenv是一个python工具. 它可以创建一个独立的python环境. 这样做的好处是你的python程序运行在这个环境里, 不受其它的 python library的版本问题影响. 比如说你想使用最新的Django 1.4开发新的项目, 但有部分第三方扩展库依赖1.1的版本。或者是系统升级了扩展库, 你的程序也直接受到的兼容性的影响。

使用 VirtualEnv 的理由：

* 隔离项目之间的第三方包依赖，如A项目依赖django1.2.5，B项目依赖django1.3。 
* 为部署应用提供方便，把开发环境的虚拟环境打包到生产环境即可,不需要在服务器上再折腾一翻。

类似功能的工具还有_buildout : http://www.buildout.org

VirtualENV使用FAQ
=================
# 激活虚拟python环境后，运行脚本出现ImportERROR。

ImportERROR通常是由于Python无法找到扩展库造成的。为解决这个问题，最简单的方法是查看PYTHONPATH的设置是否正确。在VirtualENV环境中，由于没有提供PYTHONPATH的修改，因此可以通过修改activate.bat和deactivate.bat方便每次的使用。两个批处理文件修改的代码如下

* activate.bat

	::

		set _OLD_PYTHONPATH=%PYTHONPATH%
		set PYTHONPATH=d:\pve\Lib\site-packages

* deactivate.bat

	::
		if defined _OLD_PYTHONPATH (
			set PYTHONPATH=%_OLD_PYTHONPATH%
			set _OLD_PYTHONPATH=
		)
		if not defined _OLD_PYTHONPATH 	set PYTHONPATH=


