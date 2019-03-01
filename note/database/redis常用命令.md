Redis常用命令
==================

## 一、字符串

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