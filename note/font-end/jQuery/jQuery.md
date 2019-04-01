jQuery
========================

# 一、基本选择器
### id选择器
* $('#id').css('background', 'blue')

### 标签选择器
* $('p').css('background', 'blue')

### class选择器
* $('.className').css('background', 'blue')

### 选择所有
* $('*')

# 二、层次选择器
### div 下的 span
* $('div span').css(...)

### 紧挨着 input 的 span
* $('input + span').css(...)

# 三、属性选择器
### 选择 input 的 type = "password"的标签，选择 input 的 name = "email"
* $('input[type=password]') // 选择 input 的 type = "password"的标签
* $('input[name=email]')    // 选择 input 的 name = "email"
* $('input[name^=sku]')     // 选择input 的 name 开头 = sku的（正则表达式）
* $('input[name*=sk]')      // 选择 input 的 name 含有 sk 的

# 四、 内容过滤器
### 选择 td 标签下的 内容含有“女”的标签 <td>女</td>
* $('td:contains(女)')
### 选择 td 标签下的内容为空的标签
* $('td:empty')
### 选择 td 标签下的内容不为空:有父标签资格的
* $('td:parent')
### 选择 td 下含有span的
* $('td:has(span)')

# 五、表单类型过滤器
### input type = "xxx"
* $('input:xxx')