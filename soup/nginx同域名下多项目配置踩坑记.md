nginx同域名访问不同版本的php和不同的项目
=====================================

## 问题
* 入职新公司负责重构原有项目，引入新框架。涉及到用户体系打通的问题，公司早年项目图快，使用了大概八九年前的`ecshop`进行开发。最开始因为只有微信h5，就使用cookie和seesion来做用户认证，后来要做支付宝小程序，用户体系却要兼容原有的，就使用了`oauth2:token`认证。所有地方都采用了静默授权，所以用户登录状态是一定不能丢失的。验证流程大致是：先取session，session没有则取token，token也没有则进行用户注册。
* 那么问题来了，如果新框架使用新域名，那么怎么接入原来的用户体系呢？想过这么做单点登录：因为session都存储在redis中，那么我们可以把sessionId存cookie，然后用cookie的作用域来共享sessionId。这样理论上是可以做单点登录，但是小程序是禁用cookie的，所以这个被pass掉。

## 解决方案
* 所以我考虑使用同一域名，用Nginx做反向代理来将请求分发到不同的项目之中。

## nginx server块配置一：
* 开始想着两个项目并行，存放于某一目录下统一管理，这样比较方便，也比较灵活，项目增加会更方便。新项目用php-7.1，老项目用php-5.6，所以将php-pfm端口号分别改成了9071和9056两个。下面上server块的配置方案：
```
server {
    listen       80;
    server_name  0.0.0.0;
    index        index.php;

    location  ^~ /web/ {
    	root /home/ubuntu/www/yii/;
	    index index.php;
	    fastcgi_pass 127.0.0.1:9071;
	    try_files $uri $uri/ @web;
	    fastcgi_index index.php;
	    fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
	    include fastcgi_params;
    }

    location @web {
	    rewrite /web/(.*)$ /web/index.php?/$1 last;
    }

    location ^~ /eshop/ {
	    root /home/ubuntu/www/;
	    index index.php;
	    fastcgi_pass  127.0.0.1:9056;
	    fastcgi_index index.php;
	    fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
	    include fastcgi_params;
    }
}
```
## nginx server块配置二
* 初入公司，本着稳定压倒一切的心理思想。如果项目能在同一目录下同一管理固然好。但是前端接口都要改，而且后端中用到了不少类似于`ROOT_PATH`的变量，用这个变量来表示nginx root指向的路径，如果修改nginx的root指向，现有项目极有可能出问题。所以我最后决定把引入的新框架放在原来的eshop目录中。
* 因为eshop的每个.php文件就是一个网页，算是多入口的过程式编程项目，所以每个.php文件直接交给fpm去处理就行。但是现代php MVC框架，一般都是单入口的，靠着类似名为index.php的文件来创建路由之类的。所以直接指向会出问题，最后踩坑踩了许久，才把配置文件写好。下面上配置文件:
```
server {
    listen       80;
    server_name  0.0.0.0;
    index        index.php;
    root         /home/ubuntu/www/eshop;

    location  ^~ /web/ {
	root /home/ubuntu/www/eshop/yii;
	index index.php;
    try_files $uri $uri/ @web;

	location ~ \.php$ {
			fastcgi_pass 127.0.0.1:9071;
        	try_files $uri $uri/ @web;
        	fastcgi_index index.php;
        	fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
        	include fastcgi_params;
		}
    }

    location @web {
		rewrite /web/(.*)$ /web/index.php?/$1 last;
    }

    location ~ \.php$ {
		root /home/ubuntu/www/eshop;
		index test.php;
		fastcgi_pass  127.0.0.1:9056;
		fastcgi_index index.php;
		fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
		include fastcgi_params;
    }
}
```
## 踩坑
### 1.静态资源加载问题
* 原因很多，但是解决的的思想很简单。如果是404，说明你的root或者alias或者rewrite写的不对。如果是403，一般来说，可能是文件夹权限不够，也可能是nginx.conf的用户（user）和你实际上的user不一样（常见nobody和root的坑，不过我没遇见过）。这里有一个网上说的很少的坑，大家注意啦。__fpm也是可以接管静态资源的，如果你把配置写到了一起，那么fpm会去接管静态资源，一般会因为各种配置问题报错403。我们要的是nginx做静态资源服务器，所以这就是我在配置二中location匹配到web之后继续写了一个location，这是为了让nginx去管理静态资源，fmp只去负责.php的动态资源__。
### 2.try_files的坑
* 这个坑坑了我很久，我把配置一写完之后，想着稍微改改就能投入使用了，结果在新框架(yii2)的时候，除了能访问到默认欢迎页，其他美化路由全部404，后来才发现。为了避免fpm接管静态资源的坑单独写了location去匹配.php。最开始没有在location匹配.php的那块之外写try_files，所以nginx一直会去找浏览上的输入地址，没有进入下面的rewrite重写那一块，所以一直导致404。最后给上面也加上try_files之后，全部正常。
## 调试心得
* 多用nginx的return，默认语法是`return httpCode xxxxx`，比如`return 200 hello $uri`。
* 打开nginx的error.log和access.log，尤其是access.log。可以去查询一下nginx的内置变量，然后输出到accesslog，很多都会调试极有帮助。下面附上几个比较有用的：
```
$args                    #请求中的参数值
$query_string            #同 $args
$arg_NAME                #GET请求中NAME的值
$is_args                 #如果请求中有参数，值为"?"，否则为空字符串
$uri                     #请求中的当前URI(不带请求参数，参数位于$args)，可以不同于浏览器传递的$request_uri的值，它可以通过内部重定向，或者使用index指令进行修改，$uri不包含主机名，如"/foo/bar.html"。
$document_uri            #同 $uri
$document_root           #当前请求的文档根目录或别名
$host                    #优先级：HTTP请求行的主机名>"HOST"请求头字段>符合请求的服务器名
$hostname                #主机名
$https                   #如果开启了SSL安全模式，值为"on"，否则为空字符串。
$binary_remote_addr      #客户端地址的二进制形式，固定长度为4个字节
$body_bytes_sent         #传输给客户端的字节数，响应头不计算在内；这个变量和Apache的mod_log_config模块中的"%B"参数保持兼容
$bytes_sent              #传输给客户端的字节数
$connection              #TCP连接的序列号
$connection_requests     #TCP连接当前的请求数量
$content_length          #"Content-Length" 请求头字段
$content_type            #"Content-Type" 请求头字段
$cookie_name             #cookie名称
$limit_rate              #用于设置响应的速度限制
$msec                    #当前的Unix时间戳
$nginx_version           #nginx版本
$pid                     #工作进程的PID
$pipe                    #如果请求来自管道通信，值为"p"，否则为"."
$proxy_protocol_addr     #获取代理访问服务器的客户端地址，如果是直接访问，该值为空字符串
$realpath_root           #当前请求的文档根目录或别名的真实路径，会将所有符号连接转换为真实路径
$remote_addr             #客户端地址
$remote_port             #客户端端口
$remote_user             #用于HTTP基础认证服务的用户名
$request                 #代表客户端的请求地址
$request_body            #客户端的请求主体：此变量可在location中使用，将请求主体通过proxy_pass，fastcgi_pass，uwsgi_pass和scgi_pass传递给下一级的代理服务器
$request_body_file       #将客户端请求主体保存在临时文件中。文件处理结束后，此文件需删除。如果需要之一开启此功能，需要设置client_body_in_file_only。如果将次文件传递给后端的代理服务器，需要禁用request body，即设置proxy_pass_request_body off，fastcgi_pass_request_body off，uwsgi_pass_request_body off，or scgi_pass_request_body off
$request_completion      #如果请求成功，值为"OK"，如果请求未完成或者请求不是一个范围请求的最后一部分，则为空
$request_filename        #当前连接请求的文件路径，由root或alias指令与URI请求生成
$request_length          #请求的长度 (包括请求的地址，http请求头和请求主体)
$request_method          #HTTP请求方法，通常为"GET"或"POST"
$request_time            #处理客户端请求使用的时间; 从读取客户端的第一个字节开始计时
$request_uri             #这个变量等于包含一些客户端请求参数的原始URI，它无法修改，请查看$uri更改或重写URI，不包含主机名，例如："/cnphp/test.php?arg=freemouse"
$scheme                  #请求使用的Web协议，"http" 或 "https"
$server_addr             #服务器端地址，需要注意的是：为了避免访问linux系统内核，应将ip地址提前设置在配置文件中
$server_name             #服务器名
$server_port             #服务器端口
$server_protocol         #服务器的HTTP版本，通常为 "HTTP/1.0" 或 "HTTP/1.1"
$status                  #HTTP响应代码
$time_iso8601            #服务器时间的ISO 8610格式
$time_local              #服务器时间（LOG Format 格式）
$cookie_NAME             #客户端请求Header头中的cookie变量，前缀"$cookie_"加上cookie名称的变量，该变量的值即为cookie名称的值
$http_NAME               #匹配任意请求头字段；变量名中的后半部分NAME可以替换成任意请求头字段，如在配置文件中需要获取http请求头："Accept-Language"，$http_accept_language即可
$http_cookie
$http_post
$http_referer
$http_user_agent
$http_x_forwarded_for
$sent_http_NAME          #可以设置任意http响应头字段；变量名中的后半部分NAME可以替换成任意响应头字段，如需要设置响应头Content-length，$sent_http_content_length即可
$sent_http_cache_control
$sent_http_connection
$sent_http_content_type
$sent_http_keep_alive
$sent_http_last_modified
$sent_http_location
$sent_http_transfer_encoding
```


