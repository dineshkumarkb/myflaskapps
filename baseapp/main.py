from flask import Flask
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route("/")
def index():
    return "<h1>This is a Base App</h1>"


if __name__ == "__main__":
    app.run()
