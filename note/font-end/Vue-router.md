Vue前端路由
====================

## 一、路由
* 后端路由：对于普通网站，所有的超链接都是url地址，对应的是服务器上的资源。
* 前端路由：对于单页面应用来说，主要通过url中的hash符号（#）来实现不同页面的切换。同时，hash请求有一个特点：HTTP请求中不会包含hash相关的内容，所以单页面应用跳转主要用hash实现。这种路由被称为前端路由。

## 二、安装
```
npm install vue-router
```
* 模块化中使用如webpack
```
import Vue form 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
```

## 三、使用
* 实例化 VueRouter 对象
```
...

<div id="app">

    // router-link 会被渲染成一个 <a> 标签
    <router-link to="/login">登录</router-link>
    <router-link to="/register">注册</router-link>

    // vue-router提供的路由容器，专门用来当占位符的，匹配到的组件会展示到里面
    <router-view><router-view> 
</div>

...

<script>
    var login = {
        template: '<h1>登录组件</h1>'
    }

    var register = {
        template: '<h2>注册组件</h2>'
    }

    var routerObj = new VueRouter({
        routes: [
            // path表示监听的路由地址，commponent表示如果匹配到path则调用相应的组件
            // 重定向 redirect 访问 / 时候，会重定向到 /login
            { path: '/', redirect: '/login'}
            { path: '/login', component: login },
            { path: '/register', component: register}
        ]
    })

    var vm = new Vue({
        el: '#app',
        data: {},
        methods: {},
        router: routerObj, // 建立对应关系
    })
</script>

...
```