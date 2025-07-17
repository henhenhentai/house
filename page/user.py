from flask import Flask, Blueprint, render_template

# 创建蓝图，蓝图名称为index_page
user_page = Blueprint('user_page', __name__)

@user_page.route('/user')
def index():
    return render_template('user.html')
