JS中获取当前元素所在的标签
=======================

# 示例
```
<a onclick="getElement(this)"></a>

<script>

function getElement(obj)
{
    alert(obj.innerHTML); 
}

</script>

```
