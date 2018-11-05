from flask_restful import Resource, marshal, fields
from ..common.db_connector.models import User

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'nickname': fields.String,
    'register_time': fields.DateTime,
    'is_admin': fields.Boolean
}


class Account(Resource):
    def get(self, uid):
        q_user = User.query.get(uid)
        return marshal(q_user, user_fields)

    def put(self):
        pass
