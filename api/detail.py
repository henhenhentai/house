from flask import Blueprint, jsonify
from models import House
from sqlalchemy import func
from datetime import datetime, timedelta
from static.house.utils import linear_model
detail_api = Blueprint('detail_api', __name__)

# 户型占比，饼图
@detail_api.route('/piedata/<block>', methods=['post'])
def pie_data(block):
    # 按房型统计分组，倒序排序
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(House.rooms).order_by(func.count().desc()).all()
    data = []
    for item in result:
        data.append({'name' : item[0], 'value': item[1]})
    return jsonify({'code': 0, 'msg': '查询出来', 'data': data})

@detail_api.route('/columndata/<block>', methods=['post'])
def column_data(block):
    # 按房型统计分组，倒序排序
    result = House.query.with_entities(House.address, func.count()).filter(House.block == block).group_by(House.address).order_by(func.count().desc()).limit(20).all()

    name = []
    list = []
    for addr ,num in result:
        addr_name= addr.rsplit('-',1)[1]
        name.append(addr_name)
        list.append(num)

    data = {
        "name": name,
        "list": list
    }
    return jsonify({'code': 1, 'msg': '查询出来', 'data': data})


@detail_api.route('/brokenlinedata/<block>', methods=['post'])
def broken_line_data(block):

    time_stamp = House.query.with_entities(House.publish_time).filter(House.block == block).all()
    date_list = []
    for i in range(1,14):

        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        day = latest_release + timedelta(days = -i)
        date_list.append(day.strftime("%m,%d"))
    date_list.reverse()
    roomdata1 = []
    roomdata2 = []
    roomdata3 = []
    roomdata4 = []
    rooms1 = House.query.with_entities(func.avg(House.price/House.area)).filter(House.block == block,House.rooms =='1室1厅').group_by(House.publish_time).order_by(House.publish_time).all()
    for item in rooms1[-14:]:
        roomdata1.append(round(item[0],2))

    rooms2 = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,House.rooms == '2室1厅').group_by(House.publish_time).order_by(House.publish_time).all()
    for item in rooms2[-14:]:
        roomdata2.append(round(item[0], 2))

    rooms3 = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,House.rooms == '2室2厅').group_by(House.publish_time).order_by(House.publish_time).all()
    for item in rooms3[-14:]:
        roomdata3.append(round(item[0], 2))

    rooms4 = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,House.rooms == '3室2厅').group_by(House.publish_time).order_by(House.publish_time).all()
    for item in rooms4[-14:]:
        roomdata4.append(round(item[0], 2))


    return jsonify({'code': 1, 'msg': '查询出来', 'data':{
              '1室1厅':roomdata1,
              '2室1厅':roomdata2,
              '2室2厅':roomdata3,
              '3室2厅':roomdata4,
              'date_li':date_list
    } })


@detail_api.route('/scatterdata/<block>', methods=['post'])
def scatter_data(block):
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block).group_by(House.publish_time).order_by(House.publish_time).all()
    time_stamp = House.query.with_entities(House.publish_time).filter(House.block ==block).all()
    time_stamp.sort(reverse = True)
    date_list = []
    for i in range(1,30):
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        day = latest_release + timedelta(days = -i)

    date_list.reverse()

    data = []
    x = []
    y= []

    for index, i in enumerate(result):
        x.append([index])
        y.append(round(i[0],2))
        data.append([index,round(i[0],2)])


    predict_value = len(data)
    predict_outcome = linear_model.linear_model_main(x, y, predict_value)

    p_outcome = round(predict_outcome[0],2)

    data.append([predict_value, p_outcome])

    return jsonify({'code': 1, 'msg': '查询出来', 'data': {
        'data-predict':data,
        'date_li':date_list
    }})
