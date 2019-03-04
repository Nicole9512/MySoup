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
* 返回值：执行命令之后，列表的长度。
```
# 加入单个元素

redis> LPUSH languages python
(integer) 1

# 加入重复元素

redis> LPUSH languages python
(integer) 2

redis> LRANGE languages 0 -1     # 列表允许重复元素
1) "python"
2) "python"

# 加入多个元素

redis> LPUSH mylist a b c
(integer) 3

redis> LRANGE mylist 0 -1
1) "c"
2) "b"
3) "a"
```

### LPUSHX
* 将值 value 插入到列表 key 的表头，当且仅当 key 存在并且是一个列表。
* 和 LPUSH key value [value …] 命令相反，当 key 不存在时， LPUSHX 命令什么也不做。
* 返回值：执行命令之后，列表的长度。
 ```
# 对空列表执行 LPUSHX

redis> LLEN greet                       # greet 是一个空列表
(integer) 0

redis> LPUSHX greet "hello"             # 尝试 LPUSHX，失败，因为列表为空
(integer) 0

# 对非空列表执行 LPUSHX

redis> LPUSH greet "hello"              # 先用 LPUSH 创建一个有一个元素的列表
(integer) 1

redis> LPUSHX greet "good morning"      # 这次 LPUSHX 执行成功
(integer) 2

redis> LRANGE greet 0 -1
1) "good morning"
2) "hello"
 ```

### RPUSH
* 将一个或多个值 value 插入到列表 key 的表尾(最右边)。
* 如果有多个 value 值，那么各个 value 值按从左到右的顺序依次插入到表尾：比如对一个空列表 mylist 执行 RPUSH mylist a b c ，得出的结果列表为 a b c ，等同于执行命令 RPUSH mylist a 、 RPUSH mylist b 、 RPUSH mylist c 。
* 如果 key 不存在，一个空列表会被创建并执行 RPUSH 操作。
* 当 key 存在但不是列表类型时，返回一个错误。
* 返回值：执行命令之后，列表的长度。
```
# 添加单个元素

redis> RPUSH languages c
(integer) 1

# 添加重复元素

redis> RPUSH languages c
(integer) 2

redis> LRANGE languages 0 -1 # 列表允许重复元素
1) "c"
2) "c"

# 添加多个元素

redis> RPUSH mylist a b c
(integer) 3

redis> LRANGE mylist 0 -1
1) "a"
2) "b"
3) "c"
```

### RPUSHX
* 将值 value 插入到列表 key 的表尾，当且仅当 key 存在并且是一个列表。
* 和 RPUSH key value [value …] 命令相反，当 key 不存在时， RPUSHX 命令什么也不做。
* RPUSHX 命令执行之后，表的长度。
```
# key不存在

redis> LLEN greet
(integer) 0

redis> RPUSHX greet "hello"     # 对不存在的 key 进行 RPUSHX，PUSH 失败。
(integer) 0

# key 存在且是一个非空列表

redis> RPUSH greet "hi"         # 先用 RPUSH 插入一个元素
(integer) 1

redis> RPUSHX greet "hello"     # greet 现在是一个列表类型，RPUSHX 操作成功。
(integer) 2

redis> LRANGE greet 0 -1
1) "hi"
2) "hello"
```

### LPOP
* 移除并返回列表 key 的头元素。
* 列表的头元素。 当 key 不存在时，返回 nil 。
```
redis> LLEN course
(integer) 0

redis> RPUSH course algorithm001
(integer) 1

redis> RPUSH course c++101
(integer) 2

redis> LPOP course  # 移除头元素
"algorithm001"
```

### RPOP
* 移除并返回列表 key 的尾元素。
* 列表的尾元素。 当 key 不存在时，返回 nil 。
```
redis> RPUSH mylist "one"
(integer) 1

redis> RPUSH mylist "two"
(integer) 2

redis> RPUSH mylist "three"
(integer) 3

redis> RPOP mylist           # 返回被弹出的元素
"three"

redis> LRANGE mylist 0 -1    # 列表剩下的元素
1) "one"
2) "two"
```

### LREM
* 根据参数 count 的值，移除列表中与参数 value 相等的元素。
* 时间复杂度： O(N)， N 为列表的长度。
* 根据参数 count 的值，移除列表中与参数 value 相等的元素。
* count 的值可以是以下几种：
    > count > 0 : 从表头开始向表尾搜索，移除与 value 相等的元素，数量为 count 。
    > count < 0 : 从表尾开始向表头搜索，移除与 value 相等的元素，数量为 count 的绝对值。
    > count = 0 : 移除表中所有与 value 相等的值。
* 返回值：被移除元素的数量。 因为不存在的 key 被视作空表(empty list)，所以当 key 不存在时， LREM 命令总是返回 0 。
```
# 先创建一个表，内容排列是
# morning hello morning helllo morning

redis> LPUSH greet "morning"
(integer) 1
redis> LPUSH greet "hello"
(integer) 2
redis> LPUSH greet "morning"
(integer) 3
redis> LPUSH greet "hello"
(integer) 4
redis> LPUSH greet "morning"
(integer) 5

redis> LRANGE greet 0 4         # 查看所有元素
1) "morning"
2) "hello"
3) "morning"
4) "hello"
5) "morning"

redis> LREM greet 2 morning     # 移除从表头到表尾，最先发现的两个 morning
(integer) 2                     # 两个元素被移除

redis> LLEN greet               # 还剩 3 个元素
(integer) 3

redis> LRANGE greet 0 2
1) "hello"
2) "hello"
3) "morning"

redis> LREM greet -1 morning    # 移除从表尾到表头，第一个 morning
(integer) 1

redis> LLEN greet               # 剩下两个元素
(integer) 2

redis> LRANGE greet 0 1
1) "hello"
2) "hello"

redis> LREM greet 0 hello      # 移除表中所有 hello
(integer) 2                    # 两个 hello 被移除

redis> LLEN greet
(integer) 0
```

### LLEN
* 返回列表 key 的长度。
* 返回值：如果 key 不存在，则 key 被解释为一个空列表，返回 0 。如果 key 不是列表类型，返回一个错误。
```
# 空列表

redis> LLEN job
(integer) 0

# 非空列表

redis> LPUSH job "cook food"
(integer) 1

redis> LPUSH job "have lunch"
(integer) 2

redis> LLEN job
(integer) 2
```

### LINDEX
* 返回列表 key 中，下标为 index 的元素。
* 下标(index)参数 start 和 stop 都以 0 为底，也就是说，以 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
* 你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
* 时间复杂度：O(N)， N 为到达下标 index 过程中经过的元素数量。因此，对列表的头元素和尾元素执行 LINDEX 命令，复杂度为O(1)。
* 如果 key 不是列表类型，返回一个错误。
* 返回值：列表中下标为 index 的元素。 如果 index 参数的值不在列表的区间范围内(out of range)，返回 nil 。
```
redis> LPUSH mylist "World"
(integer) 1

redis> LPUSH mylist "Hello"
(integer) 2

redis> LINDEX mylist 0
"Hello"

redis> LINDEX mylist -1
"World"

redis> LINDEX mylist 3        # index不在 mylist 的区间范围内
(nil)
```

### LINSERT
* 将值 value 插入到列表 key 当中，位于值 pivot 之前或之后。
* 当 pivot 不存在于列表 key 时，不执行任何操作。
* 当 key 不存在时， key 被视为空列表，不执行任何操作。
* 如果 key 不是列表类型，返回一个错误。
* 时间复杂度: O(N)， N 为寻找 pivot 过程中经过的元素数量。
* 返回值：如果命令执行成功，返回插入操作完成之后，列表的长度。 如果没有找到 pivot ，返回 -1 。 如果 key 不存在或为空列表，返回 0 。
```
redis> RPUSH mylist "Hello"
(integer) 1

redis> RPUSH mylist "World"
(integer) 2

redis> LINSERT mylist BEFORE "World" "There"
(integer) 3

redis> LRANGE mylist 0 -1
1) "Hello"
2) "There"
3) "World"
 
# 对一个非空列表插入，查找一个不存在的 pivot

redis> LINSERT mylist BEFORE "go" "let's"
(integer) -1                                    # 失败

# 对一个空列表执行 LINSERT 命令

redis> EXISTS fake_list
(integer) 0

redis> LINSERT fake_list BEFORE "nono" "gogogog"
(integer) 0                                     # 失败
```

### LSET key index value
* 将列表 key 下标为 index 的元素的值设置为 value 。
* 当 index 参数超出范围，或对一个空列表( key 不存在)进行 LSET 时，返回一个错误。
```
# 对空列表(key 不存在)进行 LSET

redis> EXISTS list
(integer) 0

redis> LSET list 0 item
(error) ERR no such key

# 对非空列表进行 LSET

redis> LPUSH job "cook food"
(integer) 1

redis> LRANGE job 0 0
1) "cook food"

redis> LSET job 0 "play game"
OK

redis> LRANGE job  0 0
1) "play game"

# index 超出范围

redis> LLEN list                    # 列表长度为 1
(integer) 1

redis> LSET list 3 'out of range'
(error) ERR index out of range
```

### LRANGE key start stop
* 返回列表 key 中指定区间内的元素，区间以偏移量 start 和 stop 指定。
* 下标(index)参数 start 和 stop 都以 0 为底，也就是说，以 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
* 你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
* LRANGE 的索引右边区间为闭区间，即`LRANGE key 0 1`，会返回两个数字。