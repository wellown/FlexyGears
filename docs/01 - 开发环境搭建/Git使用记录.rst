========================================
Git使用记录
========================================

Git服务器应用程序
========================================
目前已经有不少Git服务器端的程序可以用来自主搭建Git服务器环境。下面是收集到的一些个人认为不错的。记录以备后用。

* CGit：http://hjemli.net/git/cgit/
* GitBlit：http://www.gitblit.com

Cygwin下通过HTTP代理访问Git服务
========================================
办公环境中访问外网需要通过代理。在使用git时需要使用HTTP代理。为了在cygwin中正常使用git访问github，需要进行一些设置。

1. 创建公私钥
执行如下命令::

	ssh-keygen -r rsa

该命令将在~/.ssh目录中创建公私钥文件。对于命令行中的各个问题，一路回车就行了。

如果已经有了现成的公私钥文件，也可以直接拷贝到.ssh目录下使用。但可能会出现如下错误::

	Agent admitted failure to sign using the key.

解决的方法是执行如下命令，将密钥（文件名是id_rsa）添加到授权列表中::

	ssh-add ~/.ssh/id_rsa

2. 安装代理软件
在Cygwin中建立通过HTTP代理使用ssh需要安装corkscrew软件，在Ubantu中，使用如下命令安装::

	sudo apt-get install corkscrew

3. 编写配置文件
在.ssh目录中编写文件名为config的配置文件。文件内容如下::

	Host github.com
	User git
	Hostname ssh.github.com
	Port 443
	ProxyCommand corkscrew proxy.cmcc 8080 %h %p
	IdentityFile /home/ZhangXiaojing/.ssh/id_rsa
	
4. 验证配置是否成功
执行ssh命令，如果看到如下内容就算成功了::

	zhangxiaojing@ubuntu:~/.ssh$ ssh git@github.com
	PTY allocation request failed on channel 0
	Hi wellown! You've successfully authenticated, but GitHub does not provide shell access.
	Connection to ssh.github.com closed.
