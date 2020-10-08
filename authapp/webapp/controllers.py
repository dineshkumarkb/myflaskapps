from flask import Blueprint, render_template, url_for
from flask.views import View
from .forms import UserForm

blog = Blueprint(name="blog", import_name=__name__, url_prefix="/blog")


@blog.route("/")
def index_page():

    return "<html><h1> Index Page<h1><html>"


class UserPost(View):

    methods = ["GET", "POST"]

    def dispatch_request(self):

        myform = UserForm()
        if myform.validate_on_submit():
            user_name = myform.name.data
            print(f" Received username {user_name} ")
            return render_template(url_for("index_page"))
        return render_template("landing.html", form=myform)




