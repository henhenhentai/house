from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

# 创建flask-sqlalchemy的实例对象
db = SQLAlchemy()

class Config:
    # 调试模式
    DEBUG = False
    # 指定数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mima.@127.0.0.1/house'
    # 关闭警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = True
