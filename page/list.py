from flask import Flask, Blueprint, render_template
from models import House,Recommend;
import math

list_page = Blueprint('list_page', __name__)

@list_page.route('/list/pattern/<int:page>')
def index(page):
    # 获取房源总数
    house_total = House.query.count()
    # 计算页码数，向上取整
    total_num  = math.ceil(house_total / 10)

    # 查询每一页的数据  paginate两个参数，一个是当前页，一个每页显示的数量
    result = House.query.order_by(House.publish_time.desc()).paginate(page=page,per_page=10)

    return render_template('list.html', page_num = result.page, house_list=result.items, total_num=total_num)


@list_page.route('/list/hot_house/<int:page>')
def hot(page):
    # 获取房源总数
    house_total = House.query.count()
    # 计算页码数，向上取整
    total_num = math.ceil(house_total / 10)

    # 查询每一页的数据  paginate两个参数，一个是当前页，一个每页显示的数量
    result = House.query.order_by(House.page_views.desc()).paginate(page=page, per_page=10)

   # result = House.query.order_by(House.publish_time.desc()).paginate(page=page, per_page=10)

    return render_template('list.html', page_num=result.page, house_list=result.items, total_num=total_num)
