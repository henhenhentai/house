from flask import Flask, Blueprint, render_template, redirect
from models import House;

detail_page = Blueprint('detail_page', __name__)


@detail_page.route('/house/<int:hid>')
def index(hid):
    # 从数据库中查找房源ID为hid的房源对象
    house = House.query.get(hid)
    if house:
        # 获取房源对象的配套设施信息
        facilities = house.facilities
        # 将配套设施以-作为分割保存在列表facilities_list中
        facilities_list = facilities.split('-')

        # 定义一个用来存放推荐房源的列表变量
        recommend_list = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).limit(
            6).all()

        return render_template('detail.html', house=house, facilities=facilities_list, recommend=recommend_list)
    else:
        return redirect('/')


# 处理交通有无的情况
def deal_none(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word


detail_page.add_app_template_filter(deal_none, 'dealNone')