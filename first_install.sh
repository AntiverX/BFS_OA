#!/bin/bash
if [ -d env ];then
    cd env
    echo "进入env文件夹"
    else
    mkdir env
    cd env
    echo "env文件夹不存在"
fi
if [ -d BFS_OA ];then
    echo "python虚拟环境已存在"
    source BFS_OA/bin/activate
    else
    echo "开始创建python虚拟环境"
    virtualenv BFS_OA --python=python3
    source BFS_OA/bin/activate
    pip install django
fi
cd ..
find . -path "*/main_site/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/topic_manager/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/user_info/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/weekly_summary/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*.pyc"  -delete
if [ -f db.sqlite3 ];then
    rm db.sqlite3
fi
python manage.py makemigrations
python manage.py migrate
python manage.py install
chmod 777 db.sqlite3
sudo systemctl restart apache2