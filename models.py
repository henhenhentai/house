from config import db

# user_info表的模型类
# 存储用户信息
class User(db.Model):
    #表名
    __tablename__ = "user_info"
    # 用户ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户昵称
    name = db.Column(db.String(100))
    # 用户密码
    password = db.Column(db.String(255))
    # 邮箱地址
    email = db.Column(db.String(100))
    # 用户住址
    addr = db.Column(db.String(100))
    # 收藏房源ID
    collect_id = db.Column(db.String(250))
    # 用户浏览记录
    seen_id = db.Column(db.String(250))

    # 重写repr方法
    def __repr__(self):
        return 'User: %s, %s ' % (self.name, self.id)