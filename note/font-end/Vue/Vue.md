Vue.js
=================

# Vue对象
```
new Vue {
    el: #id
    data: {
        content: "hello, world",
    },
    methods: {
        click: function {
            alert('弹窗')
        }
    }
}
```

# 一、插值表达式
* {{ msg }}，插值表达式中的内容会被自动转义

# 二、v-cloak v-text v-html 基本用法
* v-cloak解决插值闪烁
    > <p v-cloak>{{ content }}</p>
* v-text默认是没有闪烁问题的，但是会覆盖元素中原本的text内容,但是插值表达式不会，会自动转义。
    > <p v-text="msg">text</p>
* v-html指令加入后，也会覆盖text，但是不会被自动转义。
    > <h1 v-html="这里会输出">
    >    <p>这里会输出一个段落</p>
    > </h1>

# 三、v-bind: 缩写是:
* 用于绑定属性，里面可以书写js表达式。
    > <input type="button" value="按钮" v-bind:title="myTitle">

# 四、v-on: 缩写是 @
* 用于绑定事件。
    > <input type="button" value="按钮" v-bind:title="myTitle" v-on:click="click">