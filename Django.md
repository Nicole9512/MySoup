在Django框架外的脚本中引用Django的orm方法：
在要引用的脚本头部写入:



import os, sys, django
BASE_DIR = os.path.dirname(os.path.abspath(__abspath__))
# django项目根目录
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
# django的settings文件
django.setup()
