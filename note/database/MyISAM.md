MyISAM
=================

# 一、简介
* MyISAM 是 MySQL 5.0之前的默认存储引擎。MyISAM 不支持事务、也不支持外键，其优势是访 问的速度快，对事务完整性没有要求或者以 SELECT、INSERT 为主的应用基本上都可以使用这个引擎来创建表。

# 二、结构
* 每个 MyISAM 在磁盘上存储成 3 个文件，其文件名都和表名相同，但扩展名分别是: 
```
 .frm(存储表定义);
 .MYD(MYData，存储数据);
 .MYI (MYIndex，存储索引)。
```
* 数据文件和索引文件可以放置在不同的目录，平均分布 IO，获得更快的速度。

# 三、异常
* MyISAM 类型的表可能会损坏，原因可能是多种多样的，损坏后的表可能不能访问，会提示需要修复或者访问后返回错误的结果。MyISAM 类型的表提供修复的工具，可以用 CHECK TABLE 语句来检查 MyISAM 表的健康，并用 REPAIR TABLE 语句修复一个损坏的 MyISAM 表。 表损坏可能导致数据库异常重新启动，需要尽快修复并尽可能地确认损坏的原因。

# 四、存储格式
MyISAM 的表又支持 3 种不同的存储格式，分别是：静态(固定长度)表，动态表，压缩表。
## 1.静态表
* 静态表是默认的存储格式。静态表中的字段都是非变长字段，这样每个记录都是固定长度的，这种存储方式的优点是存储非常迅速，容易缓存，出现故障容易恢复;缺点是占用的空间通常比动态表多。静态表的数据在存储的时候会按照列的宽度定义补足空格，但 是在应用访问的时候并不会得到这些空格，这些空格在返回给应用之前已经去掉。
* 但是也有些需要特别注意的问题，如果需要保存的内容后面本来就带有空格，那么在返 回结果的时候也会被去掉，开发人员在编写程序的时候需要特别注意，因为静态表是默认的 存储格式，开发人员可能并没有意识到这一点，从而丢失了尾部的空格。
## 2.动态表
* 动态表中包含变长字段，记录不是固定长度的，这样存储的优点是占用的空间相对较少，但 是频繁地更新删除记录会产生碎片，需要定期执行 OPTIMIZE TABLE 语句或 myisamchk -r 命 令来改善性能，并且出现故障的时候恢复相对比较困难。
## 3.压缩表
* 压缩表由 myisampack 工具创建，占据非常小的磁盘空间。因为每个记录是被单独压缩的，所以只有非常小的访问开支。
