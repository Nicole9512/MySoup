php.ini文件的配置的小坑

## 一、最好不要开启session_autostart
* 因为这样会导致`session_name()`不能使用，有时候这是一个比较坑的事情。比如说，项目迁移的时候SESSIONID不一样。必要的时候，可以选择在web脚本入口执行`session_start()`。
