## 运行

1、运行前端vue项目yun_dir

输入命令：

 `cnpm install`

 `npm run serve`



2、本地运行Django项目NAS_Django

`python manage.py migrate`

`python manage.py runserver 127.0.0.1:8003`

或使用uwsgi启动

编辑后端目录下的uwsgi.ini文件

启动命令

`uwsgi -ini uwsgi.ini`



3、nginx配置



## 功能说明
1、文件管理，视频观看，图片预览，文本编辑等功能。
2、离线下载，可以通过提交种子链接，在服务器内自动开启下载。
3、用户隔离，利用nginx隔开各个用户的物理储存地址，保证用户的安全性。
4、服务器性能监控，提供可视化直观的显示系统性能使用，使用动态线形图展示服务器网络使用情况。