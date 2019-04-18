yii2的yii\redis\session扩展
======================================

## 问题
* 因为项目重构迁移，之前用户的session都是直接通过PHP自带的`$_SESSION`来存储的，>迁移到yii2之后，发现`$session = Yii::$app->session;`的实例居然取不到和`$_SESSION`。

## 原因
* `yii\redis\session`扩展中，对`PHPSESSID`做了处理，变成了形如`f17aaec6c78cf9da9308348b0808939eb11cc`的样子。
* 原生的`$_SESSION`存储的`PHPSESSID`是`PHPREDIS_SESSION:k7cgakqa9tg4sj26jp4ak11p86`这个样子的。如果使用了`yii\redis\session`扩展，那么连`$_SESSION`也会被修改掉>。
* 这样就导致了web页面上显示的`PHPSESSID`和实际存储在的redis的是不一样的，所以取>不出来。

## 解决方案
* 使用`yii\web\sesssion`来处理session，通过php.ini来设置session的存储位置即可。
