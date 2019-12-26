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

#### 修改配置文件

备份配置文件

```
cp 000-default.conf 000-default.conf.bak
```

删除配置文件

```
rm 000-default.conf
```

使用lrzsz拖入新的配置文件（注意修改相关的路径）

#### 设置charset

将`/etc/apache2/conf-available/charset.conf`中的

```
# AddDefaultCharset UTF-8
```

更改为

```
AddDefaultCharset UTF-8
```

然后重启Apache2

```
sudo systemctl restart apache2
```

将`/etc/apache2/envvar`中的

```
export LANG=C
```

修改为

```
# export LANG=C
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
```

然后重启Apache2

```
sudo systemctl restart apache2
```
### 配置mysql

#### 创建数据库，设置root的用户名和密码

```
mysql -u root
CREATE DATABASE BFS_OA CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
set password for 'root'@'localhost' = PASSWORD('mySecretPassword'); 
FLUSH PRIVILEGES;
service mysql restart
```

#### 创建相关的初始化数据

python manage.py makemigrations xxx，这里的xxx是app的名字，由于[第一次初始化时django不会自动侦测app的情况](https://stackoverflow.com/questions/36153748/django-makemigrations-no-changes-detected)，django在migration的时候可能无法识别app中的models，这时就需要手动把app的名字加在这上面

install是我自己写的一个命令，相关内容保存在main_site/management/commands/install.py中，这个命令主要是完成了搭建系统时的一些初始化工作

```
python manage.py makemigrations user_info main_site newcomer topic_manager_v2
python manage.py migrate
python manage.py install
```

### 配置虚拟网卡

初始情况我们一般会把第一块网卡接在校园网上

但为了Linux能够连接到内网，就需要添加一块额外的网卡

获得第二块网卡的名字
```
ls /sys/class/net
```

将`/etc/netplan/`中的配置文件（默认情况下只有一个文件）从

```
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    ens32:
      dhcp4: yes
      dhcp6: yes
```

修改为

```
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    ens32:
      dhcp4: yes
      dhcp6: yes
    ens36:
      addresses:
        - 192.168.2.11/24
      gateway4: 192.168.2.1
```

一定要注意里面的缩进和空格数量，该对齐的必须对齐，否则就会出现如下的错误。错误的原因是我的`gateway4`前面多加了两个空格

```
/etc/netplan/01-netcfg.yaml:13:9: Invalid YAML: did not find expected '-' indicator:
        gateway4: 192.168.2.1
        ^
```

然后运行下面的命令使更改生效

```
sudo netplan apply
```

命令生效之后可能会出现无法通过`SSH`连接的情况，这是因为做完上述的网络配置更改之后，netplan自动添加了一条路由

从VMware里连接实验室的服务器，进入这个虚拟机运行下述命令删除这条默认路由

```
sudo route del -net 0.0.0.0/0 gw 192.168.2.1
```

路由表就会从

```
antiver@subject:~$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.2.1     0.0.0.0         UG    100    0        0 ens36
0.0.0.0         10.15.8.1       0.0.0.0         UG    100    0        0 ens32
10.15.8.0       0.0.0.0         255.255.254.0   U     0      0        0 ens32
10.15.8.1       0.0.0.0         255.255.255.255 UH    100    0        0 ens32
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 ens36
```

变更为

```
antiver@subject:~$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.15.8.1       0.0.0.0         UG    100    0        0 ens32
10.15.8.0       0.0.0.0         255.255.254.0   U     0      0        0 ens32
10.15.8.1       0.0.0.0         255.255.255.255 UH    100    0        0 ens32
192.168.2.0     0.0.0.0         255.255.255.0   U     0      0        0 ens36
```

这样子Linux的流量会优先从ens32网卡经过，就能正常地通过校园网连接到这个Linux虚拟机

### 创建必要的文件夹
```
mkdir  /var/www/html/BFS_OA/static/file/topic_manager/
sudo chmod -R 777 /var/www/html/BFS_OA/static/file/topic_manager/
sudo chmod -R 777 /var/www/html/BFS_OA
```


