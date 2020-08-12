from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
import platform,os, sys


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class Employee(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    __tablename__ = "employee"

    def __init__(self, username, **kwargs):
        super(Employee, self).__init__(username,**kwargs)
        self.username = username

    def __repr__(self):
        return f" Employee {self.username} "



@app.route("/")
def index():
    return "<h1>This is a Base App</h1>"


if __name__ == "__main__":
    app.run()
