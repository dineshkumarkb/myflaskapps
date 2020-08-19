from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_migrate import Migrate
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    print(f" The recent values are {recent}")
    top_tags = db.session.query(Tag, func.count(tags.c.post_id)).label('total').join(tags).group_by(
        Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags




@app.route("/", methods=['GET'])
def index():
    return '<h1>This is a base postgress app</h1>'


@app.route("/<int:page>", methods=['GET'])
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page,
                                                                   app.config['POSTS_PER_PAGE'],
                                                                   error_out=False)
    print(f" The post value is {posts}")
    recent, top_tags = sidebar_data()
    render_template('home.html',
                    posts=posts,
                    recent=recent,
                    top_tags=top_tags)


class Employee(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20),nullable=False)
    posts = db.relationship('Post',
                            backref='employee',
                            lazy='dynamic')

    __tablename__ = "employee"

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)

    def __repr__(self):
        return f"Employee {self.username}"

tags = db.Table('post_tags', db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    comments = db.relationship('Comment',
                               backref='post',
                               lazy='dynamic')
    tags = db.relationship('Tag',
                           secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        #self.title = title

    def __repr__(self):
        return f"Post {self.title}"


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Comment {self.name}"





class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Tag {self.name}"






if __name__ == "__main__":
    app.run()
