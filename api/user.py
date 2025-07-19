from flask import Blueprint, request, Response, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import json
from models import User
from config import db



user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['post'])
def register():

    # 判断用户是否注册
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    # 密码加密
    password = generate_password_hash(password)

    # 查询所有的用户名
    result = User.query.filter(User.name == name).all()

    # 如果查询出来的数据长度为0的话，则该用户名没有被注册过
    if len(result) == 0:
        user = User(name=name, password=password, email=email);
        # 将用户对象添加到数据库当中
        db.session.add(user)
        db.session.commit()

        #json_str = json.dumps({'code': 1, 'msg': '注册成功', 'data': user.name})
        json_str = json.dumps({'code': 1, 'msg':  user.name})
        # 实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        # 存储用户数据,设置过期时间
        res.set_cookie('name', user.name, 3600 * 24 * 7)
        return res
    else:

        return jsonify({'code': 0, 'msg': '该用户已被注册'})

@user_api.route('/login', methods=['post'])
def login():
    name = request.form['username']
    password = request.form['password']

    result = User.query.filter(User.name == name).first()

    print(result)
    if result:
        if not check_password_hash(result.password, password):
            return jsonify({'code': 0, 'msg': '密码错误'})
        else:
            json_str = json.dumps({'code': 1, 'msg': '登陆成功', 'data': result.name})
            res = Response(json_str)
            res.set_cookie('name', result.name, 3600 * 24 * 7)
            return res
    else:
        return jsonify({'code': 0, 'msg': '用户不存在'})




#登出
@user_api.route('/logout', methods=['post'])
def logout():
    name = request.cookies.get('name')
    if name:
        json_str = json.dumps({'code': 1, 'msg': '退出登录成功'})
        res = Response(json_str)
        # 删除存储的用户信信息
        res.set_cookie('name', '', expires=0)
        return res
    else:
        return jsonify({'code': 0, 'msg': '未登陆，请先去登陆'})


# 基本资料
@user_api.route('/profile', methods=['post'])
def profile():
    # 获取cookies存储的数据
    username = request.cookies.get('name')
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    addr = request.form['addr']

    user = User.query.filter(User.name == username).first()
    if user:
        data = {
            'name': name,
            'email': email,
            "addr": addr
        }
        # 判断是否修改密码
        if password:
            password = generate_password_hash(password)
            data['password'] = password

        db.session.query(User).filter_by(id=user.id).update(data)
        db.session.commit()
        json_str = json.dumps({'code': 1, 'msg': '修改成功', 'data': name})
        res = Response(json_str)
        res.set_cookie('name', name)
        return res
    else:
        return jsonify({'code': 0, 'msg': '用户不存在'})


