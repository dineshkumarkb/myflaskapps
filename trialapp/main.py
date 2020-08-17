from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(DevConfig)


@app.route("/", methods=['GET'])
def index():
    return f"<h1>This is my trial app</h1>"


class Restaurant(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Restaurant {self.name}, {self.id}"


if __name__ == "__main__":
    app.run()

