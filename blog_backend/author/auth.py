import functools
from flask import Blueprint, request, session, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from ..common.db_connector.models import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['post'])
def login():
    """
    用户登录

    参数：
    {
        'username': 'USERNAME',
        'password': '123'
    }
    """
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username)

    if not user:
        return jsonify({'success': False,
                        'msg': 'Username not exist!'})

    if not check_password_hash(user.password, password):
        return jsonify({'success': False,
                        'msg': 'Incorrect password!'})

    session.clear()
    session['user_id'] = user.id

    return jsonify({'success': True,
                    'msg': 'Login success'})


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
        g.user = User.query.get(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'success': False,
                            'msg': 'User not login'})

        return view(**kwargs)

    return wrapped_view
