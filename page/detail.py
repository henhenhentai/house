from flask import Flask, Blueprint, render_template, redirect, request, jsonify, Response
from models import House, User;
from config import db  # SQLAlchemy 数据库实例，用于数据库操作。
import json

detail_page = Blueprint('detail_page', __name__)


@detail_page.route('/house/<int:hid>')
def index(hid):
    # 查询房源
    house = House.query.get(hid)
    if not house:
        return redirect('/')

    # … 你的其他原有代码 …
    # … 获取name和user对象 …
    name = request.cookies.get('name')
    user = User.query.filter(User.name == name).first()
    collection_status = False
    if user:
        collect_id = user.collect_id
        collect = collect_id.split(',') if collect_id else []
        collection_status = True if str(hid) in collect else False

        # ==================【新增：添加浏览记录】==================
        seen_id = user.seen_id
        seen = seen_id.split(',') if seen_id else []
        hid_str = str(hid)
        # 如果已存在这条浏览，则移至最前（去重）
        if hid_str in seen:
            seen.remove(hid_str)
        seen.insert(0, hid_str)      # 最新的放最前面

        # 只保留最近20条
        seen = seen[:20]

        # 保存到数据库
        user.seen_id = ','.join(seen)
        db.session.commit()
        # ==================【新增完毕】==================

    # 获取配套设施
    facilities = house.facilities
    facilities_list = facilities.split('-') if facilities else []

    # 推荐房源
    recommend_list = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).limit(6).all()

    return render_template('detail.html', house=house, facilities=facilities_list, recommend=recommend_list,
                           collection=collection_status)


# 处理交通有无的情况
def deal_none(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word



@detail_page.route('/collection/<int:hid>', methods=['POST'])
def collection(hid):
    house = House.query.get(hid)
    if house:
        # 获取用户信息
        name = request.cookies.get('name')
        user = User.query.filter(User.name == name).first()

        if user:
            collect_id = user.collect_id
            collect = collect_id.split(',') if collect_id else []
            msg = ''
            # 已收藏
            if str(hid) in collect:
                collect.remove(str(hid))
                msg = "取消收藏成功"

            # 未收藏
            else:
                collect.append(str(hid))
                data = {
                    'collect_id': ','.join(collect)
                }
                msg = "收藏成功"
            data = {
                'collect_id': ','.join(collect)
            }
            db.session.query(User).filter_by(id=user.id).update(data)
            db.session.commit()
            json_str = json.dumps({'code': 1, 'msg': msg, 'data': ''})
            res = Response(json_str)
            return res

        else:
            return jsonify({'code': 0, 'msg': '未登录，请先去登录'})

    else:
        return redirect('/')

@detail_page.route('/seen/clear', methods=['POST'])
def clear_seen():
    name = request.cookies.get('name')
    user = User.query.filter_by(name=name).first()
    if not user:
        return jsonify({'code': 0, 'msg': '未登录，请先登录！'})
    user.seen_id = ''
    db.session.commit()
    return jsonify({'code': 1, 'msg': '浏览记录已清空！'})

detail_page.add_app_template_filter(deal_none, 'dealNone')