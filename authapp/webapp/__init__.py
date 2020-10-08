from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app():

    from .controllers import blog, UserPost
    from authapp.config import DevConfig
    app = Flask(__name__)
    app.config.from_object(DevConfig())
    app.register_blueprint(blog)
    app.add_url_rule("/createuser", view_func=UserPost.as_view("userpost"))
    db.init_app(app)

    return app