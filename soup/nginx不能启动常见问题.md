nginx不能启动常见问题
======================

## 一、语法错误
### 1.表现
* `nginx -t`之后，不能提示successful，会提示`syntax...`类似的话。
### 2.解决
* 查看具体报错信息，这种最简单，一般是语法错误。

## 二、端口被占用
### 1.表现
* `service nginx start`后会有提示让你查看，经常体现在类似`0.0.0.0[::80]`之类的形式。
### 2.解决
* 干掉占用端口的进程。

## 三、启动一小会儿nginx报超时错误
### 1.表现
* `service nginx start`后会有提示让你查看，例如这样
```
Apr 02 14:37:01 VM-0-13-ubuntu systemd[1]: Starting A high performance web server and a reverse proxy server...
Apr 02 14:37:01 VM-0-13-ubuntu systemd[1]: nginx.service: PID file /run/nginx.pid not readable (yet?) after start: No such file or directory
Apr 02 14:38:31 VM-0-13-ubuntu systemd[1]: nginx.service: Start operation timed out. Terminating.
Apr 02 14:38:31 VM-0-13-ubuntu systemd[1]: Failed to start A high performance web server and a reverse proxy server.
Apr 02 14:38:31 VM-0-13-ubuntu systemd[1]: nginx.service: Unit entered failed state.
Apr 02 14:38:31 VM-0-13-ubuntu systemd[1]: nginx.service: Failed with result 'timeout'.
```
### 2.解决
* `nginx.conf`文件的pid路径和`service.nginx`的pid路径不相同。

