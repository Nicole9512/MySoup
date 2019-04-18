MySQL修改密码总提示错误(Ubuntu)
=============================

## 问题
* MySQL5.7 for Ubuntu 的版本会默认有一个随即密码，路径在`/etc/mysql/debian.cnf`这里可以查看。
* 登入MySQL之后，可以这么更改root密码:
```
use mysql;
update user set authentication_string=password("你的密码") where user="root";
```
* 修改成功之后执行`mysql -uroot -p`，会发现密码改掉了却登陆不上去。

## 解决
* 找到配置文件并修改`sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf`，在`[mysqld]`这一块中加入`skip-grant-tables`，重启MySQL服务，解决问题。


