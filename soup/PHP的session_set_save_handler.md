PHP中自定义session储存过程

## 自定义$_SESSION`
* 强烈不推荐自己重新定义原来的$_SESSION全局变量。这样会给项目扩展，伸缩性带来很>多问题。那么，要自定义$_SEESION，就要使用到了PHP内置的`session_set_save_handler`函数。
* 函数详情可以去查询PHP手册，下面简单介绍。

## session_set_save_handler
* 该函数需要5.4及以上的PHP版本。函数有两种原型，我们介绍步骤最多的那种，下面给出example处理类SessionHandler。
```
$handler = new SessionHandler();
session_set_save_handler(
    array($handler, 'open'),
    array($handler, 'close'),
    array($handler, 'read'),
    array($handler, 'write'),
    array($handler, 'destroy'),
    array($handler, 'gc')
    );
```

