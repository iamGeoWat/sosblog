from ..config import get_config
import pymysql

config = get_config()

# 建立数据库链接
db = pymysql.connect(config.HOST_NAME, config.USERNAME, config.PASSWORD, config.DATABASE)
