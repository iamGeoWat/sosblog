import functools
from flask import Blueprint, request, session, jsonify, g
from ..common.db_connector.mysql_connector import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['post'])
def register():
    """
    用户注册

    参数：
    {
        'username': 'USERNAME',
        'password': '123',
        'nickname': 'NICKNAME'
    }
    """
    username = request.form['username']
    password = request.form['password']

    db = get_db()


@auth_blueprint.route('/logout')
def logout():
    """
    用户登出
    """
    session.clear()
    return jsonify({'success': True,
                    'msg': 'Logout success'})


@auth_blueprint.before_app_request()
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'success': False,
                            'msg': 'User not login'})

        return view(**kwargs)

    return wrapped_view
