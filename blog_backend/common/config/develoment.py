from .default import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    """开发模式配置"""
    HOST_NAME = '127.0.0.1'
    USERNAME = 'root'
    PASSWORD = '9012343as'
    DATABASE = 'sosblog'

    # 配置flask配置对象中键：SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@" + HOST_NAME + "/" + DATABASE

    # 配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动

    SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
