from . import db, registrations
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    # 通过角色名查找现有角色然后再进行更新
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.COMMENT |
                     Permission.CHOOSE, True
                     ),
            'Administrator': (0xff, False)

        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)

        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(11))
    position = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    name = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    courses = db.relationship('Course',
                              secondary=registrations,
                              backref=db.backref('users', lazy='dynamic'),
                              lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable')

    # password为只写属性，当设置这个属性时，系统会自动调用generate_password_hash()，并把字段赋值给password_hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #返回用户所选课程
    @property
    def get_courses(self):
        return Course.query.join(User.courses.id==Course.id).filter(registrations.users_id==self.id)

    # 赋予用户觉角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == 'admin':
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # 检查是否有指定权限
    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 用户选课
    def choose_course(self, course):
        if not self.get_course(course):
            self.courses.append(course)
            db.session.commit()

    # 用户退课
    def delete_course(self, course):
        u = self.courses.filter_by(id=course.id).first()
        if u:
            self.courses.remove(u)
            db.session.commit()

    # 查看用户选择的课程
    def get_course(self, course):
        return self.courses.filter_by(id=course.id).first() is not None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Permission:
    ADMINISTER = 0x80
    COMMENT = 0X02
    CHOOSE = 0X01
    WRITE_POST = 0X04


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')


login_manager.anonymous_user = AnonymousUser


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time = db.Column(db.String(32))
