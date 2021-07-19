## 项目介绍
基于**hadoop**和**ElasticSearch**构建的简单文件检索系统

## 运行项目
### 安装环境
```angular2html
pip3 install -r requirements.txt
```

### 修改配置
在 **app/__init__.py** 中修改 hdfs 和 elasticsearch 连接
```angular2html
# 连接 hdfs
client = pyhdfs.HdfsClient(hosts='192.168.174.10:50070', user_name='root')
# 使用 elasticsearch
es = elasticsearch.Elasticsearch(['192.168.174.10'], http_auth=('user', 'password'), port=9200)
es_index = 'test'
```
在**config.py**中修改数据库连接, 并在mysql中新建相应的数据库
```angular2html
SQLALCHEMY_DATABASE_URI = 'mysql://test:123456@127.0.0.1:3306/hadoop_demo'
```

### 运行项目
```angular2html
python3 app.py
```
得到以下输出
```angular2html
 * Serving Flask app 'app.py' (lazy loading)
 * Environment: development
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
http://127.0.0.1:5000/ 为首页地址
> 注意此处还需要修改 **app/view/__init__.py** 的 **BASEURL** 为你当前的连接, 此处为 http://127.0.0.1:5000/


## 效果图
![index](../images/index.png)