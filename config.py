# 数据库
# 设置连接数据库的URL
SQLALCHEMY_DATABASE_URI = 'mysql://test:123456@127.0.0.1:3306/hadoop_demo'
# 数据库和模型类同步修改
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 查询时会显示原始SQL语句
SQLALCHEMY_ECHO = True

# ====================================================
# session
SECRET_KEY = 'netexp'