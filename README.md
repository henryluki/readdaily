readdaily
========
<img src="http://readdaily.sinaapp.com/favicon.ico"/> 每日阅读

========
- 运行于新浪云SAE引擎
- demo ：http://readdaily.sinaapp.com
- 线上成功案例：http://www.iyuedu.cc

========
####执行方法

- ①  git clone 到本地
- ②  查看 spider/settings.py文件中的数据库配置
   以下是Sae的配置，线上无需修改。
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': sae.const.MYSQL_DB,                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': sae.const.MYSQL_USER,
        'PASSWORD':sae.const.MYSQL_PASS,
        'HOST': sae.const.MYSQL_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': sae.const.MYSQL_PORT,                      # Set to empty string for default.
    }
}
```
- ③ 完成对数据库的配置后，利用命令 python manage.py syncdb 初始化数据表。不出意外的话，表名应该为article。
- ④ 接着需要填充数据，查看spider/cron.py 和spider/urls.py应该能明白是通过url的方式 ：keepData/id/ (id为int) 存储数据。

#####注意
- SAE 上需要手动初始化数据表。
- SAE 上能配置config.yaml来实现cronjob。

####技术与功能
- 后端：python 2.7 django 1.5 lxml 3.4 beautifulsoup 3.2 MySQL 
- 前端：bootstrap 3 Jquery 
- 数据库定时更新
- 移动端界面适配
