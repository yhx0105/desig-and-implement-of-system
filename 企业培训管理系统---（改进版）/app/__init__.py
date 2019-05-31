from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'Strong'
login_manager.login_view = 'auth.login'
registrations=db.Table('registrations',
                       db.Column('users_id',db.Integer,db.ForeignKey('users.id'),primary_key=True),
                       db.Column('courses_id',db.Integer,db.ForeignKey('courses.id'),primary_key=True))

# 使用工厂函数,延迟创建程序实例，把创建过程移到可显示调用的工厂函数中
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # url_prefix为可选参数，若定义了这个参数，注册后该蓝本所有路由会加上指定前缀eg:/login变为/auth/login
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
