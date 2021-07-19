from flask import Flask, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
import pyhdfs, pymysql
import elasticsearch

pymysql.install_as_MySQLdb()
app = Flask(__name__)  # type: Flask
app.config.from_object('config')
# 实例化一个数据库对象
db = SQLAlchemy(app)

# 连接 hdfs
client = pyhdfs.HdfsClient(hosts='192.168.174.10:50070', user_name='root')
# 使用 elasticsearch 代替数据库
es = elasticsearch.Elasticsearch(['192.168.174.10'], http_auth=('es', '123456'), port=9200)
# es = elasticsearch.Elasticsearch(['192.168.174.10'], http_auth=('user', 'password'), port=9200)
es_index2 = 'test2'

from . import blueprint_register
db.create_all()

if not es.indices.exists(index=es_index2):
    body = {
        "mappings": {
            "properties": {
                "filename": {
                    "type": "text"
                },
                "filepath": {
                    "type": "text"
                },
                "content": {
                    "type": "text",
                },
            }
        }
    }
    es.indices.create(index=es_index2, body=body)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/show/<path:p>', methods=["POST", "GET"])
def show(p: str):
    path = p.replace('..', '')
    return send_file(f'media/{path}')
