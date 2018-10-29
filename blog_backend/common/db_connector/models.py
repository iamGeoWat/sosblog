from .mysql_connector import get_db

db = get_db()


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    nickname = db.Column(db.String(10), nullable=False)
    register_time = db.Column(db.DateTime(), nullable=True)
    is_admin = db.Column(db.Boolean(), nullable=False)
