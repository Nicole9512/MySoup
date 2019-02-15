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


###### 4.常用的字符串处理函数
* [String](http://php.net/manual/zh/ref.strings.php)字符串函数

* [md5()](http://php.net/manual/zh/function.md5.php) 计算字符串md5的散列值
* [trim()](http://php.net/manual/zh/function.trim.php) 去处字符串首尾的空白字符`" "普通空格符, \t制表符, \n换行符, \r回车符, \0空字节符, \x0B垂直制表符`
* [strpos()](http://php.net/manual/zh/function.strpos.php) 查找字符串首次出现的位置

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
        echo "<br />";
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
        echo "<br />";
    }
}
 
Man::callself();  // output： xxxx
Man::callstatic();  // output： yyy
?>
```

###### 11.private protected public final

###### 12.OOP思想

###### 13.抽象类和接口类的使用场景

###### 14.Trait

###### 15.echo print print_r var_dump

###### 16.__construct 和 __destruct

###### 17.static作用

###### 18.__toString() 作用

###### 19.单引号与双引号的区别

###### 20.常见的Http状态码

###### 21.冒泡排序（bubble sort）
* 冒泡排序是从列表的开头处开始，并且比较一对数据项，直到移动到列表的末尾。每当成对的两项之间的排序不正确时，算法就交换其位置，依次完成排序。
```
class Sort
{
    function bubbleSort($numbers) 
    {
        $len = count($numbers);
        for ($i = 0; $i < $len - 1; $i++) {
            for ($j = 0; $j < $len - $i - 1; $j++) {
                if ($numbers[$j] > $numbers[$j + 1]) {
                    $temp = $numbers[$j];
                    $numbers[$j] = $numbers[$j + 1];
                    $numbers[$j + 1] = $temp;
                }
            }
        }
        return $numbers;
    }
}
```