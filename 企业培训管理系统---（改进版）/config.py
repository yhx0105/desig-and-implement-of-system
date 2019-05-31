import os


# basedir = os.path.abspath(os.path.dirname(__file__))
#链接mysql数据库

class Config:
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    # MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
    #                ['true', 'on', '1']
    # MAIL_USERNAME = os.environ.get('1370117133')
    # MAIL_PASSWORD = os.environ.get('hmvlwdqqdpdogaad')
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <1370117133@qq.com>'
    DEBUG = True
    SECRET_KEY = os.urandom(24)

    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'manage_sys2'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT,
                                                                           DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_POSTS_PER_PAGE = 3
    FLASKY_COURSE_PER_PAGE = 6
    FLASKY_COMMENTS_PER_PAGE = 6
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'manage_sys2'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT,
                                                                           DATABASE)



config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
