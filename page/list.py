from flask import Flask, Blueprint, render_template

# 创建蓝图，蓝图名称为index_page
list_page = Blueprint('list_page', __name__)

@list_page.route('/list')
def index():
    return render_template('list.html')





