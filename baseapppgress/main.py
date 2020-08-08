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

    __tablename__ = "employee"

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)

    def __repr__(self):
        return f"Employee {self.username}"


if __name__ == "__main__":
    app.run()
