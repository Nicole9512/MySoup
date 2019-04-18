CentOS下安装并简单配置MySQL
===========================

## 流程
### 一、删除mariadb
* centOS7自带mariadb，需要删除掉。执行完，可以查看是否存在。同理，可以查看是否自带了mysql。
```
rpm -qa | grep mariadb
rpm -e --nodeps mariadb-libs-5.5.56-2.el7.x86_64
```
### 二、下载yum源
* 下载`mysql57-community-release-el7-8.noarch.rpm`的yum源，并安装`mysql57-community-release-el7-8.noarch.rpm`
```
wget http://repo.mysql.com/mysql57-community-release-el7-8.noarch.rpm
rpm -ivh mysql57-community-release-el7-8.noarch.rpm
```
### 三、安装并启动MySQL
```
yum -y install mysql-server
systemctl start mysqld
```
### 四、找到MySQL的默认随机密码
* `cat /var/log/mysqld.log | grep password`会得到类似`A temporary password is generated for root@localhost: hilX0U!9i3_6`的信息，后面的就是随机密码，然后`mysql -uroot -p`输入密码登录。
### 五、修改密码
* 这时候要进行操作MySQL会提示让你修改密码。`ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.`。
* 大部分情况我们不需要很复杂的密码，但是MySQL会强制要你密码设置的复杂一点，这时候可以这么做：
```
set global validate_password_policy=0;
set global validate_password_length=1;
alter user 'root'@'localhost' identified by 'passwd';
ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
grant all privileges on *.* to root@"%" identified by "passwd";
grant all privileges on *.* to root@"localhost" identified by "passwd";
flush privileges;
```
到这里就全部OK啦，如果远程工具还是连接不上，可以试试`iptables -F`清除防火墙的规则。

