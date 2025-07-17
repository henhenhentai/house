from flask import Blueprint, request, jsonify
#from database import add_data,data_select,connection
import pymysql
import pymysql.cursors

connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='house',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
# 创建连接

def data_select():
    # 创建游标对象
    with connection.cursor() as cursor:
        # 执行 SQL 查询
        sql = "SELECT name , password FROM user_info"
        cursor.execute(sql)

        # 获取查询结果
        result = cursor.fetchall()

        # 打印结果
        print(result)
        return result

    # 关闭连接
    connection.close()


user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['post'])
def register():

    name = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # 1. 查询用户是否已存在
    with connection.cursor() as cursor:
        sql = "SELECT * FROM user_info WHERE name = %s"
        cursor.execute(sql, (name,))
        result = cursor.fetchone()

    if result:
        return jsonify({'valid': 0, 'msg': '该用户已被注册'})

    # 2. 如果用户不存在，则插入新用户
    try:
        with connection.cursor() as cursor:

            sql = "INSERT INTO user_info (name , password, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, password, email))
        connection.commit()
        return jsonify({'valid': 1, 'msg': '注册成功'})
    except Exception as e:
        connection.rollback()
        return jsonify({'valid': 0, 'msg': f'注册失败: {e}'})

@user_api.route('/login', methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 使用 data_select 函数查询所有用户数据
    users = data_select()

    # 遍历查询结果，进行用户验证
    for user in users:
        # 在实际应用中，密码应该被加密存储和比对
        if user['name'] == username and user['password'] == password:
            # 登录成功，可以在 session 中记录用户状态
            return jsonify({'valid': 1, 'msg': '登录成功'})

    return jsonify({'valid': 0, 'msg': '用户名或密码错误'})