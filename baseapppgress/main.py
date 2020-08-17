from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)




@app.route("/", methods=['GET'])
def index():
    return '<h1>This is a base postgress app</h1>'


class Employee(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    posts = db.relationship('Post',
                            backref='employee',
                            lazy='dynamic')

    __tablename__ = "employee"

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)

    def __repr__(self):
        return f"Employee {self.username}"


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)
        #self.title = title

    def __repr__(self):
        return f"Post {self.title}"


if __name__ == "__main__":
    app.run()
