from flask import Flask, Blueprint, render_template, request, jsonify
from models import House;
import math
query_page = Blueprint('query_page', __name__)


@query_page.route('/query')
def search_txt_info():
    # 获取地区字段的查询
    if request.args.get('addr'):
        addr = request.args.get('addr')
        result = House.query.filter(House.address == addr).order_by(House.publish_time.desc()).all()
        return render_template('search.html', house_list=result)
    # 获取户型字段的查询
    if request.args.get('rooms'):
        rooms = request.args.get('rooms')
        result = House.query.filter(House.rooms == rooms).order_by(House.publish_time.desc()).all()
        return render_template('search.html', house_list=result)
    # 默认渲染首页
    return render_template('index.html')


# 当房源标题长度大于15的时候，用省略号替代
def deal_title_over(title):
    if len(title) > 15:
        return title[:15] + '...'
    else:
        return title


# 当房源朝向，交通条件为空的时候，显示暂无信息
def deal_direction(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word


# 添加过滤器
query_page.add_app_template_filter(deal_title_over, 'dealover')
query_page.add_app_template_filter(deal_direction, 'dealdirection')

def index(page):
    # 获取房源总数
    house_total = House.query.count()
    # 计算页码数，向上取整
    total_num  = math.ceil(house_total / 10)

    # 查询每一页的数据  paginate两个参数，一个是当前页，一个每页显示的数量

    result = House.query.order_by(House.publish_time.desc()).paginate(page=page,per_page=10)

    return render_template('list.html', page_num = result.page, house_list=result.items, total_num=total_num)
