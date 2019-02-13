# Django定义模型层，自设主键时候
需要使用id = models.AutoField(primary_key=True)
而不是id = models.IntegerFiled(primary_key=True)
因为一般要指定主键时，主键为自增:
Django自带的primary_key不能直接自增，需要使用自增字段AutoField
(Django文档中未说明)


