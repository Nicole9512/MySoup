Redis常用命令
==================

# 一、字符串

### SET
* 设置键值对
```
EX seconds ： 将键的过期时间设置为 seconds 秒。 执行 SET key value EX seconds 的效果等同于执行 SETEX key seconds value 。
PX milliseconds ： 将键的过期时间设置为 milliseconds 毫秒。 执行 SET key value PX milliseconds 的效果等同于执行 PSETEX key milliseconds value 。
NX ： 只在键不存在时， 才对键进行设置操作。 执行 SET key value NX 的效果等同于执行 SETNX key value 。
XX ： 只在键已经存在时， 才对键进行设置操作。
```

### SETNX
* 只在键 key 不存在的情况下， 将键 key 的值设置为 value 。
* 存在的话不作任何操作。
* 命令在设置成功时返回 1 ， 设置失败时返回 0 。
```
redis> EXISTS job                # job 不存在
(integer) 0

redis> SETNX job "programmer"    # job 设置成功
(integer) 1

redis> SETNX job "code-farmer"   # 尝试覆盖 job ，失败
(integer) 0

redis> GET job                   # 没有被覆盖
"programmer"
```

### SETEX
* 将键 key 的值设置为 value ， 并将键 key 的生存时间设置为 seconds 秒钟。
* 如果键 key 已经存在， 那么 SETEX 命令将覆盖已有的值。
```
redis> SETEX cache_user_id 60 10086
OK

redis> GET cache_user_id  # 值
"10086"

redis> TTL cache_user_id  # 剩余生存时间
(integer) 49
```

### PSETEX
* 这个命令和 SETEX 命令相似， 但它以毫秒为单位设置 key 的生存时间， 而不是像 SETEX 命令那样以秒为单位进行设置。
```
redis> PSETEX mykey 1000 "Hello"
OK

redis> PTTL mykey
(integer) 999

redis> GET mykey
"Hello"
```

### GET
* 如果键 key 不存在， 那么返回特殊值 nil ； 否则， 返回键 key 的值。
* 如果键 key 的值并非字符串类型， 那么返回一个错误， 因为 GET 命令只能用于字符串值。
```
redis> GET db
(nil)

redis> SET db redis
OK

redis> GET db
"redis"
```

### GETSET
* 将键 key 的值设为 value ， 并返回键 key 在被设置之前的旧值。
* 如果键 key 没有旧值， 也即是说， 键 key 在被设置之前并不存在， 那么命令返回 nil 。
* 当键 key 存在但不是字符串类型时， 命令返回一个错误。
```
redis> GETSET db mongodb    # 没有旧值，返回 nil
(nil)

redis> GET db
"mongodb"

redis> GETSET db redis      # 返回旧值 mongodb
"mongodb"

redis> GET db
"redis"
```

### STRLEN
* 返回键 key 储存的字符串值的长度。
* 当键 key 不存在时， 命令返回 0 。
* 当 key 储存的不是字符串值时， 返回一个错误。
```
redis> SET mykey "Hello world"
OK

redis> STRLEN mykey
(integer) 11
```

### APPEND
* 如果键 key 已经存在并且它的值是一个字符串， APPEND 命令将把 value 追加到键 key 现有值的末尾。
* 如果 key 不存在， APPEND 就简单地将键 key 的值设为 value ， 就像执行 SET key value 一样。
* 返回值：追加 value 之后， 键 key 的值的长度。

### SETRANGE
* Redis Setrange 命令用指定的字符串覆盖给定 key 所储存的字符串值，覆盖的位置从偏移量 offset 开始。
* 返回值：SETRANGE 命令会返回被修改之后， 字符串值的长度。
* 时间复杂度：对于长度较短的字符串，命令的平摊复杂度O(1)；对于长度较大的字符串，命令的复杂度为 O(M) ，其中 M 为 value 的长度。
```
redis 127.0.0.1:6379> SET key1 "Hello World"
OK
redis 127.0.0.1:6379> SETRANGE key1 6 "Redis"
(integer) 11
redis 127.0.0.1:6379> GET key1
"Hello Redis"
```
* 不存在的键 key 当作空白字符串处理。
```
redis> EXISTS empty_string
(integer) 0

redis> SETRANGE empty_string 5 "Redis!"   # 对不存在的 key 使用 SETRANGE
(integer) 11

redis> GET empty_string                   # 空白处被"\x00"填充
"\x00\x00\x00\x00\x00Redis!"
```

### GETRANGE
* Redis Getrange 命令用于获取存储在指定 key 中字符串的子字符串。字符串的截取范围由 start 和 end 两个偏移量决定(包括 start 和 end 在内)。可以包含负数索引。GETRANGE 命令在 Redis 2.0 之前的版本里面被称为 SUBSTR 命令。
```
redis> SET greeting "hello, my friend"
OK

redis> GETRANGE greeting 0 4          # 返回索引0-4的字符，包括4。
"hello"

redis> GETRANGE greeting -1 -5        # 不支持回绕操作
""

redis> GETRANGE greeting -3 -1        # 负数索引
"end"

redis> GETRANGE greeting 0 -1         # 从第一个到最后一个
"hello, my friend"

redis> GETRANGE greeting 0 1008611    # 值域范围不超过实际字符串，超过部分自动被符略
"hello, my friend"
```

### INCR
* 为键 key 储存的数字值加上一。
* 如果键 key 不存在， 那么它的值会先被初始化为 0 ， 然后再执行 INCR 命令。
* 如果键 key 储存的值不能被解释为数字， 那么 INCR 命令将返回一个错误。
* 本操作的值限制在 64 位(bit)有符号数字表示之内。
```
redis> SET page_view 20
OK

redis> INCR page_view
(integer) 21

redis> GET page_view    # 数字值在 Redis 中以字符串的形式保存
"21"
```

### INCRBY
* 为键 key 储存的数字值加上增量 increment 。
* 本操作的值限制在 64 位(bit)有符号数字表示之内。
```
redis> SET rank 50
OK

redis> INCRBY rank 20
(integer) 70

redis> GET rank
"70"
```
* 如果键 key 不存在， 那么键 key 的值会先被初始化为 0 ， 然后再执行 INCRBY 命令。
```
redis> EXISTS counter
(integer) 0

redis> INCRBY counter 30
(integer) 30

redis> GET counter
"30"
```
* 如果键 key 储存的值不能被解释为数字， 那么 INCRBY 命令将返回一个错误。
```
redis> SET book "long long ago..."
OK

redis> INCRBY book 200
(error) ERR value is not an integer or out of range
```

### INCRBYFLOAT
* 该命令同INCRBY。
* 当以下任意一个条件发生时， 命令返回一个错误：
    > 键 key 的值不是字符串类型(因为 Redis 中的数字和浮点数都以字符串的形式保存，所以它们都属于字符串类型）；
    > 键 key 当前的值或者给定的增量 increment 不能被解释(parse)为双精度浮点数。


### DECR
* 为键 key 储存的数字值减去1。
```
redis> SET failure_times 10
OK

redis> DECR failure_times
(integer) 9
```
* 如果键 key 不存在， 那么键 key 的值会先被初始化为 0 ， 然后再执行 DECR 操作。
```
redis> EXISTS count
(integer) 0

redis> DECR count
(integer) -1
```
* 如果键 key 储存的值不能被解释为数字， 那么 DECR 命令将返回一个错误。
* 本操作的值限制在 64 位(bit)有符号数字表示之内。

### DECRBY
* 将键 key 储存的整数值减去减量 decrement 。
```
redis> SET count 100
OK

redis> DECRBY count 20
(integer) 80
```
* 如果键 key 不存在， 那么键 key 的值会先被初始化为 0 ， 然后再执行 DECRBY 命令。
```
redis> EXISTS pages
(integer) 0

redis> DECRBY pages 10
(integer) -10
```
* 如果键 key 储存的值不能被解释为数字， 那么 DECRBY 命令将返回一个错误。
* 本操作的值限制在 64 位(bit)有符号数字表示之内。 

### MSET
* 同时为多个键设置值。
* 如果某个给定键已经存在， 那么 MSET 将使用新值去覆盖旧值， 如果这不是你所希望的效果， 请考虑使用 MSETNX 命令， 这个命令只会在所有给定键都不存在的情况下进行设置。
* MSET 是一个原子性(atomic)操作， 所有给定键都会在同一时间内被设置， 不会出现某些键被设置了但是另一些键没有被设置的情况。
* 返回值：MSET 命令总是返回 OK 。
* 时间复杂度： O(N) ，其中 N 为给定键的数量。
```
redis> MSET date "2012.3.30" time "11:00 a.m." weather "sunny"
OK

redis> MGET date time weather
1) "2012.3.30"
2) "11:00 a.m."
3) "sunny"
```

### MSETNX
* 当且仅当所有给定键都不存在时， 为所有给定键设置值。
* 即使只有一个给定键已经存在， MSETNX 命令也会拒绝执行对所有键的设置操作。
* MSETNX 是一个原子性(atomic)操作， 所有给定键要么就全部都被设置， 要么就全部都不设置， 不可能出现第三种状态。
* 返回值：当所有给定键都设置成功时， 命令返回 1 ； 如果因为某个给定键已经存在而导致设置未能成功执行， 那么命令返回 0 。
* 时间复杂度： O(N) ，其中 N 为给定键的数量。

### MGET
* 返回给定的一个或多个字符串键的值。
* 如果给定的字符串键里面， 有某个键不存在， 那么这个键的值将以特殊值 nil 表示。
* 返回值：MGET 命令将返回一个列表， 列表中包含了所有给定键的值。
```
redis> SET redis redis.com
OK

redis> SET mongodb mongodb.org
OK

redis> MGET redis mongodb
1) "redis.com"
2) "mongodb.org"

redis> MGET redis mongodb mysql     # 不存在的 mysql 返回 nil
1) "redis.com"
2) "mongodb.org"
3) (nil)
```

# 二、列表（LIST）
### LPUSH 
* 将一个或多个值 value 插入到列表 key 的表头
* 如果有多个 value 值，那么各个 value 值按从左到右的顺序依次插入到表头： 比如说，对空列表 mylist 执行命令 LPUSH mylist a b c ，列表的值将是 c b a ，这等同于原子性地执行 LPUSH mylist a 、 LPUSH mylist b 和 LPUSH mylist c 三个命令。

 