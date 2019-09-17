# BFS_OA

## TODO

1. 注册完成之后的返回页面

## 部署方法

### 安装LAMP

在安装ubuntu 18.04 server时自动选择即可

```
sudo apt install libapache2-mod-wsgi-py3 lrzsz libmysqlclient-dev \
     python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip
```

### 创建python3虚拟环境

```
sudo apt install virtualenv
sudo chmod -R 777 /var/www/html
mkdir -p /var/www/html/BFS_OA/env/ && cd /var/www/html/BFS_OA/env/
virtualenv -p python3 BFS_OA
```
### 在python3虚拟环境中安装必要的软件

激活python3环境（每次调整python3环境如安装其他库，都需要运行此命令）

```
source /var/www/html/BFS_OA/env/BFS_OA/bin/activate
```

安装必要的库

```
pip install django mysqlclient
```

### 设置apache2

备份配置文件

```
cp 000-default.conf 000-default.conf.bak
```

删除配置文件

```
rm 000-default.conf
```

使用lrzsz拖入新的配置文件（注意修改相关的路径）


### 配置mysql

```
mysql -u root
CREATE DATABASE BFS_OA CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
```

### 创建相关数据库

python manage.py makemigrations xxx，这里的xxx是app的名字，由于不知名的原因，django在migration的时候可能无法识别app中的models，这时就需要手动把app的名字加在这上面

install是我自己写的一个命令，相关内容保存在main_site/management/commands/install.py中，这个命令主要是完成了搭建系统时的一些初始化工作

```
python manage.py makemigrations user_info main_site newcomer topic_manager_v2
python manage.py migrate
python manage.py install
```

