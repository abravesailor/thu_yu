# thu_yu
数据库更新方法:
1. 删除backend/migrations/ 里的000x.py文件
2. 删除 工作目录下的 sqlite3 数据库
3. 在工作目录下: 运行 python manage.py makemigrations
            python manage.py migrate

