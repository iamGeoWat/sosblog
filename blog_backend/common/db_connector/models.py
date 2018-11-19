from blog_backend.author import create_app, db
import datetime


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(10), nullable=False)
    register_time = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return self.username

    def __init__(self, username, password, nickname):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.register_time = datetime.datetime.now()
        self.is_admin = False


tags = db.Table('article_tag',
                db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Article(db.Model):
    __table_name__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(1200))
    create_time = db.Column(db.DateTime)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('articles', lazy='dynamic'))

    def __str__(self):
        return self.title

    def __init__(self, title, author, content, category):  # TODO *tags?
        self.title = title
        self.author = author
        self.content = content
        self.category = category
        self.create_time = datetime.datetime.now()

    def __repr__(self):
        return '<Article %r>' % self.title


class Tag(db.Model):
    __table_name__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(20))

    def __str__(self):
        return self.tag_name

    def __repr__(self):
        return '<Tag %r>' % self.tag_name

    def __init__(self, tag_name):
        self.tag_name = tag_name


class Category(db.Model):
    __table_name__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(20))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<category %r>' % self.cname

    def __str__(self):
        return self.cname


class Comment(db.Model):
    __table_name__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    article = db.Column(db.Integer, db.ForeignKey('article.id'))
    content = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<comment for article %r>' % self.article


if __name__ == '__main__':
    app = create_app()
    with app.test_request_context():
        user1 = User.query.all()[0]
        print(user1.is_admin)
