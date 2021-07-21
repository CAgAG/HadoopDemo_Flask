import uuid, time
import pymysql
import elasticsearch
import random
import warnings

# 忽略 warning
warnings.filterwarnings('ignore')


def run_time(func, username: str):
    start = time.time()
    func(username)
    end = time.time()
    print('the running time is', end - start, 's')


def search_sql(username: str):
    select_str = f"SELECT * FROM user WHERE username='{username}'"
    cursor.execute(select_str)


def search_es(username: str):
    data = {
        'username': username
    }
    body = {
        "query": {
            "match": data
        }
    }
    es.search(index=es_index, body=body)


if __name__ == '__main__':
    """
    mode: 1: insert, 0: search
    """
    mode = 0
    if mode == 1:
        epoch = 10000
    else:
        # 查询
        username = f'22df58f9-9428-43c7-ba0e-30b5d847cfbd'

    es = elasticsearch.Elasticsearch(['192.168.174.10'], http_auth=('es', 'password'), port=9200)
    es_index = 'hadoop_demo_exp'

    db = pymysql.connect(host="127.0.0.1", user="test", password="123456", db="hadoop_demo")
    cursor = db.cursor()

    if mode == 1:
        # 创建 index
        body = {
            "mappings": {
                "properties": {
                    "username": {
                        "type": "text"
                    },
                    "email": {
                        "type": "text"
                    },
                    "password": {
                        "type": "text"
                    },
                }
            }
        }
        if not es.indices.exists(index=es_index):
            # 创建 index
            es.indices.create(index=es_index, body=body)

        # 插入数据
        for _ in range(epoch):
            username = str(uuid.uuid4())
            password = str(random.random())
            email = f'{str(random.randint(0, epoch * 2))}@qq.com'

            # 插入数据
            data = {
                "username": username,
                "email": email,
                "password": password
            }
            insert_str = "INSERT INTO user VALUES (" + \
                         f"'{username}', '{email}', '{password}')"
            cursor.execute(insert_str)
            es.index(index=es_index, body=data)
            db.commit()
    else:
        print("sql: ")
        run_time(search_sql, username=username)
        print("es: ")
        run_time(search_es, username=username)

"""
1000
sql: 
the running time is 0.0009605884552001953 s
es: 
the running time is 0.025393009185791016 s

5000
sql: 
the running time is 0.021760940551757812 s
es: 
the running time is 0.02169060707092285 s

10000
sql: 
the running time is 0.11307048797607422 s
es: 
the running time is 0.016216516494750977 s
"""
