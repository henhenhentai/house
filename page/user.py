from flask import Blueprint, render_template, redirect
from models import User, House

user_page = Blueprint('user_page', __name__)

@user_page.route('/user/<name>')
def index(name):
    user = User.query.filter(User.name == name).first()
    if not user:
        return redirect('/')

    # 收藏
    user_collect_list = []
    user_collect_ids = user.collect_id.split(',') if user.collect_id else []
    for house_id in user_collect_ids:
        house = House.query.get(house_id)
        if house:
            user_collect_list.append(house)

    # 浏览记录
    user_seen_list = []
    user_seen_ids = user.seen_id.split(',') if user.seen_id else []
    for house_id in user_seen_ids:
        house = House.query.get(house_id)
        if house:
            user_seen_list.append(house)

    return render_template('user.html', user=user, collect=user_collect_list, seen=user_seen_list)
