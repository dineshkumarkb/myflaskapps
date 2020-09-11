from flask import Flask, flash, render_template, jsonify,redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask.views import View
from sqlalchemy.dialects.postgresql import UUID
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, Length, email_validator, InputRequired
from wtforms.fields.html5 import EmailField
from config import DevConfig
import uuid

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class UserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    email = EmailField('email', validators=[Email()])
    org = StringField('org', validators=[InputRequired()])


class UserInfo(db.Model):

    uid = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    org = db.relationship('Organization', backref='userinfo', lazy=True)

    __tablename__ = "userinfo"
    
    def __init__(self, **kwargs):
        super(UserInfo, self).__init__(**kwargs)

    def __repr__(self):
        return f"UserInfo {self.username}"


class Organization(db.Model):

    org_id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('userinfo.uid'), nullable=False)


@app.route("/index", methods=['GET', 'POST'])
def index():
    user_form = UserForm()
    print(request.method)
    if request.method == "POST":
        print(f" POST request received ")
        if user_form.validate_on_submit():
            uid = uuid.uuid4()
            name = user_form.username.data
            email = user_form.email.data
            password = user_form.password.data
            print(f" User form validated {uid}, {name}, {email}, {password}")
            usr = UserInfo(uid=uid, username=name, email=email, password=password)
            add_to_db(usr)
            return redirect(url_for('index'))

    return render_template('index.html', form=user_form)


class GenericView(View):

    def dispatch_request(self):
        return render_template("class.html")



def add_to_db(db_obj):
    try:
        db.create_all()
        db.session.add(db_obj)
        db.session.commit()

    except Exception as e:
        print(f" Error while adding to db {e}")



@app.route("/", methods=['GET', 'POST'])
def landing():
    print("Landing")
    myform = UserForm()
    if request.method == 'POST':
        if myform.validate_on_submit():
            print(f" Form validated ")
            return redirect(url_for('landing'))

    return render_template('helpers.html', form=myform)


@app.route("/getusers/<username>", methods=['GET'])
def get_users(username):
    user = UserInfo.query.filter(UserInfo.username == username).first()
    print(user)
    return jsonify({"code": 200, "username": user.username, "email": user.email, "id": user.uid})


if __name__ == "__main__":
    app.add_url_rule("/class", view_func=GenericView.as_view("generic"))
    app.run(debug=True)

