PHP常见面试题
======================

###### 1.PHP全称解释
* Hypertext Preprocessor的缩写，超文本预处理器，是一种用来开发动态网站的服务器脚本语言。

###### 2.PHP引用传递和值传递的区别
* 值传递：方法调用时，实际参数把它的值传递给对应的形式参数，函数接收的是原始值的一个copy，此时内存中存在两个相等的基本类型，即实际参数和形式参数，后面方法的操作都是对形参这个值的修改，不影响实际参数的值。
* 引用传递：也称为值传递。方法调用时，实际参数的引用(地址，而不是参数的值)被传递给方法中相对应的形式参数，函数接收的是原始值的内存地址；在方法执行中，形参和实参内容相同，指向同一块内存地址，方法执行中对引用的操作将会影响到实际对象。
* PHP中的一般都是值传递，需要引用传递时候，变量前加`&`。
* 优缺点：引用传递不需要复制，美滋滋，节约内存，有时候也会节省操作。

###### 3.常用的数组处理函数
* [Array](http://php.net/manual/zh/ref.array.php) 数组函数

* [is_array()](http://php.net/manual/zh/function.is-array.php) 判断是否是数组
* [explode()](http://php.net/manual/zh/function.explode.php) 使用一个字符串分割另外一个字符串
* [implode()](http://php.net/manual/zh/function.implode.php) 把一个一维数组转化为字符串
* [array_change_key_case()](http://php.net/manual/zh/function.array-change-key-case.php) 将数组中的所有键名修改为全大写或小写
* [array_intersect()](http://php.net/manual/zh/function.array-intersect.php) 计算数组交集
* [array_key_exists()](http://php.net/manual/zh/function.array-key-exists.php) 检查数组里是否有指定的键名或索引



###### 4.常用的字符串处理函数
* [String](http://php.net/manual/zh/ref.strings.php)字符串函数

* [md5()](http://php.net/manual/zh/function.md5.php) 计算字符串md5的散列值
* [trim()](http://php.net/manual/zh/function.trim.php) 去处字符串首尾的空白字符`" "普通空格符, \t制表符, \n换行符, \r回车符, \0空字节符, \x0B垂直制表符`
* [strpos()](http://php.net/manual/zh/function.strpos.php) 查找字符串首次出现的位置
* [strrpos()] 查找字符串最后一次出现的位置
* [str_repeat()](http://php.net/manual/zh/function.str-repeat.php) 把一个字符串重复n次
* [sprintf()](http://php.net/manual/zh/function.sprintf.php) 格式化输出字符串
* [is_numeric()](http://php.net/manual/zh/function.is-numeric.php) 检测变量是否为数字或数字字符串

###### 5.mb类函数
* 多字节字符串函数，其实就是可以处理utf8mb4的函数。PHP内置的字符串长度函数strlen无法正确处理中文字符串，它得到的只是字符串所占的字节数。对于GB2312的中文编码，strlen得到的值是汉字个数的2倍，而对于UTF-8编码的中文，就是3倍的差异了（在 UTF-8编码下，一个汉字占3个字节）。
采用mb_strlen函数可以较好地解决这个问题。mb_strlen的用法和 strlen类似，只不过它有第二个可选参数用于指定字符编码。例如得到UTF-8的字符串$str长度，可以用 mb_strlen($str,'UTF-8')。如果省略第二个参数，则会使用PHP的内部编码。内部编码可以通过 mb_internal_encoding()函数得到。
需要注意的是，mb_strlen并不是PHP核心函数，Windows 下使用前需要确保在php.ini中加载了php_mbstring.dll，即确保“extension=php_mbstring.dll”这一行存在并且没有被注释掉，否则会出现未定义函数的问题。Linux 下需要编译这个扩展。

###### 6.&引用传递，实际案例

###### 7. == 与 === 
* ===是包括变量值与类型完全相等，而==只是比较两个数的值是否相等。
比如：100==“100” 这里用==，因为它们的值相等，都是100，结果为真
但是若用===，因为左边是一个整型而右边则是一个字符串类型的数，类型不相同所以结果为假。

###### 8.isset() 与 empty()
* isset()检测变量是否设置。如果变量不存在返回false，如果变量存在但是值为null也返回false。使用unset()释放掉变量之后，isset()返回false，PHP函数isset()只能用于变量，传递其他参数都将解析错误。检测常量可以用defined()函数。
* empty()检测变量是否为空。其中，变量存在且值为""、0、"0"、NULL、、FALSE、array()、var $var; 以及没有任何属性的对象，返回true。

###### 9.魔术方法
* [魔术方法](http://www.php.net/manual/zh/language.oop5.magic.php)
* __construct() 构造函数：一个类中定义一个方法作为构造函数。具有构造函数的类会在每次创建新对象（实例化）时先调用此方法，所以非常适合在使用对象之前做一些初始化工作。
* __set() 在给不可访问属性赋值时，会被调用。经常利用于动态绑定属性。
* __get() 读取不可访问属性的值时，__get() 会被调用。
```
<?php

class Person
{
    public $name = '周伯通';
    private $_sex = '男';

    function __set($property, $val)
    {
        echo '个人信息: ' . $property . ' ' . $val . PHP_EOL;
    }

    function __get($property)
    {
        echo '取得信息: ' . $property . PHP_EOL;
    }
}

$class = new Person();
// 这调用__set() 输出 个人信息: 女
$class->_sex = '女';
// 这里调用__get() 输出 取得信息: 女
$class->_sex;
// 这里如果是$class->name, 这样的话会就没有权限控制, 对本类来说__get, __set可以添加额外的方法达到另外一些效果
// 例如这样，动态绑定一些属性
$class->age = '18岁';

class People
{
    public $name = '李莫愁';
    private $_sex = '女';

    function __set($name, $val)
    {
        $this->$name = '个人信息: ' . $val . PHP_EOL;
    }

    function getSex()
    {
        echo $this->_sex;
    }
}

$class = new People();
$class->_sex = '变态';
echo $class->getSex(); // 个人信息: 变态
```
* __toString() 该方法用于一个类被当成字符串使用时候怎样回应，该方法必须返回字符串。
* __isset() 当对不可访问属性调用 isset() 或 empty() 时，__isset() 会被调用。
* __unset() 当对不可访问属性调用 unset() 时，__unset() 会被调用。


###### 10.static this self 区别
* 注意点：静态方法执行之后变量的值不会丢失，只会初始化一次，这个值对所有实例都是有效的。
```
静态方法执行后生成的对象，就相当于一个实例，可以调用$this的所有方法。
$statConnect = StatConnect::loadFor($user_id, $product_id, $time, $type);
$statConnect->updateAttributes(['carts' => $num]);
```
* `static`和`self`不存在继承时候，完全相同。存在继承关系时候，self调用的方法和属性始终表示当前类的方法和属性，static调用的方法和属性为当前执行的类的方法和属性。简单通俗的来说，self就是写在哪个类里面, 实际调用的就是这个类。static代表使用的这个类, 就是你在父类里写的static,然后被子类覆盖，使用的就是子类的方法或属性。
```
<?php
class Person
{
    public static function name()
    {
        echo "xxx";
    }
    public static function callself()
    {
        self::name();
    }
 
    public static function callstatic()
    {
        static::name();
    }
}
 
class Man extends Person
{
    public static function name()
    {
        echo "yyy";
    }
}
 
Man::callself();  // output： xxxx
Man::callstatic();  // output： yyy
?>
```

###### 11.private protected public final

###### 12.OOP思想
* 面向对象程序设计（英语：Object-oriented programming，缩写：OOP）是种具有对象概念的程序编程典范，同时也是一种程序开发的抽象方针。它可能包含数据、属性、代码与方法。对象则指的是类的实例。它将对象作为程序的基本单元，将程序和数据封装其中，以提高软件的重用性、灵活性和扩展性，对象里的程序可以访问及经常修改对象相关连的数据。在面向对象程序编程里，计算机程序会被设计成彼此相关的对象。
* __类__ ：定义了一件事物的抽象特点。类的定义包含了数据的形式以及对数据的操作。
* __对象__ ：类的实例。
* __封装性__ ：具备封装性（Encapsulation）的面向对象编程隐藏了某一方法的具体运行步骤，取而代之的是通过消息传递机制发送消息给它。封装是通过限制只有特定类的对象可以访问这一特定类的成员，而它们通常利用接口实现消息的传入传出。举个例子，接口能确保幼犬这一特征只能被赋予狗这一类。通常来说，成员会依它们的访问权限被分为3种：公有成员、私有成员以及保护成员。
* __继承__ ：继承性（Inheritance）是指，在某种情况下，一个类会有“子类”。子类一般来说比父类要更加具体化。子类自动继承父类的所有除了private之外的所有属性和方法。
* __多态__ ：
* __抽象性__ ：抽象（Abstraction）是简化复杂的现实问题的途径，它可以为具体问题找到最恰当的类定义，并且可以在最恰当的继承级别解释问题。

###### 13.抽象类和接口类的使用场景

###### 14.Trait
* 从基类继承的成员会被trait插入的成员覆盖。优先顺序是来自当前类的成员覆盖了trait的方法，而trait覆盖被继承的方法。多个trait都插入了同名方法的话。会产生错误。需要用insteadof操作符来指定。trait可以使用抽象方法来做强制要求。

###### 15.echo print print_r var_dump
* echo 输出由逗号分隔的一个或者多个字符串，没有返回值。
* print() 只能输出一个字符串，并且是比较简单的数据类型比如string int，返回值为1.
* print_r() 输出一个人类可读的表示方式，不仅接收数组和对象，还能将他们格式化可读。如果给出第二个参数，可以将其输出作为返回值返回。
* var_dump() 类似于print_r()，但是还会显示打印纸的类型，没有返回值。
* echo 与 print() 是语言结构。

###### 16.__construct 和 __destruct

###### 17.static作用

###### 18.

###### 19.单引号与双引号的区别
* 单引号不解释变量，双引号解释变量。
* 双引号里插入单引号，其中单引号里如果有变量的话，变量解释。
* 双引号的变量名后面必须要有一个非数字、字母、下划线的特殊字符，或者用{}讲变量括起来，否则会将变量名后面的部分当做一个整体，引起语法错误。
* 双引号解释转义字符，单引号不解释转义字符，但是解释'\和\。
* 能使单引号字符尽量使用单引号，单引号的效率比双引号要高（因为双引号要先遍历一遍，判断里面有没有变量，然后再进行操作，而单引号则不需要判断）。

###### 20.常见的Http状态码
* 200 : 请求成功，请求的数据随之返回。
* 301 : 永久性重定向。
* 302 : 暂时行重定向。
* 401 : 当前请求需要用户验证。
* 403 : 服务器拒绝执行请求，即没有权限。
* 404 : 请求失败，请求的数据在服务器上未发现。
* 500 : 服务器错误。一般服务器端程序执行错误。
* 502 : nginx找不到php-fpm或者资源耗尽(php-fpm连接全部用完)
* 503 : 服务器临时维护或过载。这个状态时临时性的。
* 504 : 请求超时。

###### 21.冒泡排序（bubble sort）
* 冒泡排序是从列表的开头处开始，并且比较一对数据项，直到移动到列表的末尾。每当成对的两项之间的排序不正确时，算法就交换其位置，依次完成排序。
```
<?php

class Sort
{
    function bubbleSort($numbers) 
    {
        $len = count($numbers);
        for ($i = 0; $i < $len - 1; $i++) {
            for ($j = 0; $j < $len - $i - 1; $j++) {
                if ($numbers[$j] > $numbers[$j + 1]) {
                    $this->swap($numbers, $i, $j)
                }
            }
        }
        return $numbers;
    }
}
```

##### 22.$_SERVER
* $_SERVER 是一个包含了诸如头信息(header)、路径(path)、以及脚本位置(script locations)等等信息的数组。这个数组中的项目由 Web 服务器创建。
* 'GATEWAY_INTERFACE' 服务器使用的 CGI 规范的版本；例如，“CGI/1.1”。
* 'SERVER_PROTOCOL' 请求页面时通信协议的名称和版本。例如，“HTTP/1.0”。
* 'REQUEST_METHOD' 访问页面使用的请求方法；例如，“GET”, “HEAD”，“POST”，“PUT”。
* 'HTTP_ACCEPT_CHARSET' 当前请求头中 Accept-Charset: 项的内容，如果存在的话。例如：“iso-8859-1,*,utf-8”。
* 'HTTP_ACCEPT_ENCODING' 当前请求头中 Accept-Encoding: 项的内容，如果存在的话。例如：“gzip”。
* 'HTTP_ACCEPT_LANGUAGE' 当前请求头中 Accept-Language: 项的内容，如果存在的话。例如：“en”。
* 'HTTP_CONNECTION' 当前请求头中 Connection: 项的内容，如果存在的话。例如：“Keep-Alive”。
* 'HTTP_HOST' 当前请求头中 Host: 项的内容，如果存在的话。
* 'SCRIPT_NAME' 包含当前脚本的路径。这在页面需要指向自己时非常有用。__FILE__ 常量包含当前脚本(例如包含文件)的完整路径和文件名。

* 'SERVER_ADDR' 服务器的ip地址。
* 'SERVER_NAME' 服务器名称。
* 'REQUEST_TIME' 请求开始时的时间戳。从 PHP 5.1.0 起可用。
* 'QUERY_STRING' query string（查询字符串），如果有的话，通过它进行页面访问。
* 'HTTP_REFERER' 上一次请求的页面，从哪儿来的
* 'HTTP_ACCEPT' 当前请求头中 Accept: 项的内容，如果存在的话。
* 'HTTP_USER_AGENT' 请求头信息。
* 'REMOTE_ADDR' 浏览当前页面的用户的 IP 地址。
* 'REQUEST_URI' URI 用来指定要访问的页面。例如 “/index.html”。
* 'PATH_INFO' 充当URL路径。？？

##### 23.重写
* final修饰的类方法不可被子类重写。
* PHP是否重写父类方法只会根据方法名是否一致判断（5.3以后重写父类方法参数个数必须一致）。
* 重写时访问级别只可以等于或者宽松于父类，不可提升访问级别。

##### 24.是否 ?> 结束
* 主要防止 include，require 引用文件，把文件末尾可能的回车和空格等字符引用进来，还有一些函数必须在没有任何输出之前调用，就会造成不是期望的结果。PHP文件的编码不包含BOM的UTF8. 这也是PSR-2中的规范：纯PHP代码文件必须省略最后的 ?> 结束标签。

##### 25.什么是 CGI？什么是 FastCGI？php-fpm，FastCGI，Nginx 之间是什么关系？
* CGI，通用网关接口，用于WEB服务器和应用程序间的交互，定义输入输出规范，用户的请求通过WEB服务器转发给FastCGI进程，FastCGI进程再调用应用程序进行处理，如php解析器，应用程序的处理结果如html返回给FastCGI，FastCGI返回给Nginx 进行输出。假设这里WEB服务器是Nginx，应用程序是 PHP，而 php-fpm 是管理 FastCGI 的，这也就是 php-fpm，FastCGI，和 Nginx 之间的关系。
* FastCGI 用来提高 cgi 程序性能，启动一个master，再启动多个 worker，不需要每次解析 php.ini. 而 php-fpm 实现了 FastCGI 协议，是 FastCGI 的进程管理器，支持平滑重启，可以启动的时候预先生成多个进程。

##### 26.语句include和require的区别是什么?
* 在失败的时候：
* include 产生一个 warning ，而 require 直接产生错误中断；
* require 在运行前载入；
* include 在运行时载入；
* require_once 和 include_once 可以避免重复包含同一文件。

##### 27.POST 和 GET
* get是把参数数据队列加到提交表单的action属性所指的url中，值和表单内各个字段一一对应，从url中可以看到；post是通过HTTPPOST机制，将表单内各个字段与其内容防止在HTML的head中一起传送到action属性所指的url地址，用户看不到这个过程。
* 对于get方式，服务器端用Request.QueryString获取变量的值，对于post方式，服务器端用Request.Form获取提交的数据。
* get传送的数据量较小，post传送的数据量较大，一般被默认不受限制，但在理论上，IIS4中最大量为80kb，IIS5中为1000k。
* get安全性非常低，post安全性较高。
* get比较快。

##### 28.session 与 cookie
* session:储存用户访问的全局唯一变量,存储在服务器上的php指定的目录中的（session_dir）的位置进行的存放。
* cookie:用来存储连续訪問一个頁面时所使用，是存储在客户端，对于Cookie来说是存储在用户WIN的Temp目录中的。
* 两者都可通过时间来设置时间长短。

##### 29.插入排序(Insert sort)
```
<?php

class Sort
{
    public function InsertSort(array &$arr)
    {
        //数组中第一个元素作为一个已经存在的有序表
        for ($i = 1; $i < count($arr); $i++) {
            $temp = $arr[$i];
            for ($j = $i - 1; $j >= 0 && $arr[$j] > $temp; $j--) {
                $arr[$j + 1] = $arr[$j];
            }
            $arr[$j + 1] = $temp;
        }
    }
}

```

##### 30.引用变量 &
* php中引用变量时候，只有write的时候才会进行copy*（COW机制）。object本身就是引用传递，所以不适用，要复制则需要使用clone。
```
$a = range(1, 10);

$b = $a;           // 这时候，$a和$b指向同一个内存地址，但是如果使用 $b = &$a;使用引用，那么就会指向同一内存地址。


$a = range(1, 10);  // 这时候，$a和$b在不同的内存地址

```

##### 31.unset()
* unset()只会取消引用，不会销毁内存空间。
```
$a = 1;

$b = &$a;

unset($a);

echo $b;
```

##### 32.Heredoc 和 Newdoc
* Heredoc 类似于双引号 
* Newdoc  类似于单引号

##### 33.基本数据类型相关
* float不能用于类似于等值计算等方面。（因为计算机最后进行二进制转换时候，精度会损失）

##### 34.预定义变量[超全局数组/变量]
* $_GOLBALS 
```
$GLOBALS 是PHP的一个超级全局变量组，在一个PHP脚本的全部作用域中都可以访问。
$GLOBALS 是一个包含了全部变量的全局组合数组。变量的名字就是数组的键。
```
* $_GET 
```
通过 URL 参数(QueryString)传递给当前脚本的变量的数组。
$_GET 同样被广泛应用于收集表单数据，在HTML form标签的指定该属性："method="get"。
```
* $_POST 
```
$_POST 被广泛应用于收集表单数据，在HTML form标签的指定该属性："method="post"。
```
* $_COOKIE
```
通过 HTTP Cookies 方式传递给当前脚本的变量的数组。
```
* $_SESSION
```
调用前使用session_start()
```

##### 34.预定义常量

##### 35.static
* 仅初始化一次
* 初始化时候需要赋值
* 每次执行函数该值会保留
* static修饰的变量是局部的，仅在函数内部有效
* 可以记录函数调用次数，用来结束函数递归

##### 36.正则表达式
* 作用：分割、查找、匹配、替换字符串
* 分隔符：正斜线（/）、hash符号（#）以及取反符号（~）

##### 37.文件操作
* fopen()： r/r+、w/w+、a/a+、x/x+、b、t
* fwrite()、fput()：写入
* fread()、fgets()、fgetc()：读取
* fclose()：关闭
* 不需要fopen()打开的函数：file_get_contents()、file_put_contents()
* file()：文件读取到数组
* readfile()：读取文件输出到缓冲区
* 访问远程文件allow_url_fopen，http只能读，ftp可以只读或者只写
* 名称相关：basename() dirname() pathinfo()
* 目录读取：oepndir() readdir() closedir() rewinddir()
* 目录创建删除：mkdir() rmdir()
* 文件大小：filesize()
* 文件拷贝：copy()
* 文件类型：filetype()
* 重命名目录：rename()
```
遍历删除目录下的文件
```