from flask import Blueprint, request, jsonify
from models import House # 确保您已经从 models 文件导入了 House 模型
from config import db   # 确保您已经导入了 db 实例

house_api = Blueprint('house_api', __name__)

# @house_api.route('/search', methods=['POST'])
# def search():

