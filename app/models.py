# coding:utf-8
#  import mysql.connector
from . import db


#  定义模型
class Role(db.Model):
    __tablename__='roles' # 指定表名
    role_id = db.Column(db.Integer, primary_key = True) # 定义列对象
    role_name = db.Column(db.String(20), unique = True)
    users = db.relationship('User', backref = 'role', lazy='dynamic')
    #  users属性添加到Role模型中,     用来返回与角色相关联的用户组成的列表,第一个参数表示这个关系的另一端是哪个模型
    #  backref则表示向User模型添加一个role属性,    从而定义反向关系，这个属性可替代role_id来访问Role表
    #  lazy 指定如何加载相关记录

    @staticmethod
    def seed(): #  调用这个方法就可以设置Role的默认值了
        db.session.add_all(map(lambda r:Role(role_name=r), ['guests', 'administrators']))
        db.session.commit()


class User(db.Model):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(20), nullable = False)
    #  user_email=db.Column(db.String(20), nullable = False)
    user_passwd = db.Column(db.String(20), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))# 表示该列的值是role表的id

    @staticmethod
    def on_created(target, value, initiator):
        target.role_id = Role.query.filter_by(role_name='guests').first()

    def __str__(self):
        return 'user_id:{}\tuser_name:{}\tuser_passwd:{}'.format(self.user_id, self.user_name, self.user_passwd)

#  数据库on_created事件监听 #  每插入新对象就初始化用户的Role_id为guests
db.event.listen(User.user_name, 'set', User.on_created)

