v-on事件修饰符
=================

## 一、类型
* 事件修饰符可以叠加使用，比如说`@click.prevent.once="eventName"`
__.stop__：阻止冒泡
__.prevent__：阻止默认事件
__.capture__：添加事件侦查器时使用事件捕获模式
__.self__：只当事件在该元素本身（比如说不是子元素）触发时触发事件
__.once__：只触发一次

## 二、.stop
* 触发事件默认为冒泡机制，事件触发时，会先触发B后触发A，从里到外冒泡，`.stop`修饰符可以阻止A冒泡。
* 目前理解就是阻止外层事件触发，事件终止于此。
```
...
<div id="a" @click="divA">
    <input type="button" id="b" @click="inputB"></div>
</div>
...

<script>
    触发事件...devA,inputB
</script>
```

## 三、.prevent
* 阻止默认行为，比如说阻止`<a>`标签跳转页面。

## 四、.capture
* 与冒泡相反，从外到内的顺序触发事件。

## 五、.self
* 给哪个绑定触发哪个，不管内外。