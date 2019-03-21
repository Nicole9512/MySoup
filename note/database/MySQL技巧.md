MySQL一些不太常用但是有用的知识
================================

# 一、<=> 与 =
* `<=>`安全的等于`=`，不同的是，`<=>`可以对null使用，而不用写`is null`。

# 二、事务
* MySQL 5.0 支持的存储引擎包括 MyISAM、InnoDB、BDB、MEMORY、MERGE、EXAMPLE、NDB Cluster、ARCHIVE、CSV、BLACKHOLE、FEDERATED 等，其中 InnoDB 和 BDB 提供事务安全表，其他存储引擎都是非事务安全表。


