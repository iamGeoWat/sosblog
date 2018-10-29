from flask import g, current_app
from flask_sqlalchemy import SQLAlchemy


def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)

    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    db_ob = get_db()
