from flask import Flask, Blueprint, render_template
from models import House
from config import db
# 创建蓝图，蓝图名称为index_page
index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def index():
    # 获取房源总量
    house_total_num = House.query.count()
    # 获取最新房源6条
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()
    # 获取热门房源4条
    house_hot_list = House.query.order_by(House.page_views.desc()).limit(4).all()
    return render_template('index.html', total=house_total_num, new_list=house_new_list, hot_list=house_hot_list)






