from flask import Blueprint, request, Response, jsonify
from werkzeug.security import generate_password_hash
import json
from models import User
from config import db



user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['post'])
def register():

    # 判断用户是否注册
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # 密码加密
    password = generate_password_hash(password)

    # 查询所有的用户名
    result = User.query.filter(User.name == name).first()

    # 如果查询出来的数据长度为0的话，则该用户名没有被注册过
    #if len(result) == 0:
    if result:

        return jsonify({'code': 0, 'msg': '该用户已被注册'})
    else:

        user = User(name=name, password=password, email=email);
        # 将用户对象添加到数据库当中
        db.session.add(user)
        db.session.commit()

        json_str = json.dumps({'code': 1, 'msg': user.name})
        # 实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        # 存储用户数据,设置过期时间
        res.set_cookie('name', user.name, 3600 * 24 * 7)
        return res

@user_api.route('/login', methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']

    result = User.query.filter(User.name == username , User.password == password).first()
  #  if len(result) == 1 :
    if result :
        user = User(name=username, password=password);
        json_str = json.dumps({'code': 1, 'msg': "登陆成功"})
        # 实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        # 存储用户数据,设置过期时间
        res.set_cookie('name', user.name, 3600 * 24 * 7)
        return res

    else:
        return jsonify({'code': 0, 'msg': '用户名或密码错误'})



    # users = data_select()
    #
    # # 遍历查询结果，进行用户验证
    # for user in users:
    #     # 在实际应用中，密码应该被加密存储和比对
    #     if user['name'] == username and user['password'] == password:
    #         # 登录成功，可以在 session 中记录用户状态
    #         return jsonify({'valid': 1, 'msg': '登录成功'})
    #
    # return jsonify({'valid': 0, 'msg': '用户名或密码错误'})