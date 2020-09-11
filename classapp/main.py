from flask import Flask, render_template, url_for, redirect
from flask.views import View
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, UUID, Length, Email
from wtforms.fields.html5 import EmailField
from config import DevConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity, get_current_user
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import os



app = Flask(__name__)
app.config.from_object(DevConfig())
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)


def get_uuid():
    """
    :return: employee id in UUID format
    """
    emp_id = uuid.uuid4()
    return emp_id


class EmployeeForm(FlaskForm):
    name = StringField('username', validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired(),
                                                     Length(min=3, message="Password does not match expectations")])
    email = EmailField("email", validators=[InputRequired(), Email()])


class InputProcessor(View):
    methods = ['GET', 'POST']

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        emp_form = EmployeeForm()
        if emp_form.validate_on_submit():
            emp_id = get_uuid()
            name = emp_form.name.data
            password = emp_form.password.data
            encrypted_password = bcrypt.generate_password_hash(password)
            email = emp_form.email.data
            emp_dict = dict(emp_id=get_uuid(), name=name, password=encrypted_password, email=email)
            add_employees(emp_dict=emp_dict)
            #print(f" Received emp data {emp_id}, {name}, {email}, {encrypted_password}")
            return redirect(url_for("inputprocessor"))
        return render_template(self.template_name, form=emp_form)


def add_employees(emp_dict):
    print(f" The db info is {emp_dict} ")
    emp = EmployeeData(emp_id=emp_dict.get('emp_id', None),
                   name=emp_dict.get('name', None),
                   password=emp_dict.get('password', None),
                   email=emp_dict.get('email',None))
    try:
        db.create_all()
        db.session.add(emp)
        db.session.commit()
    except Exception as e:
        print(f" Error while adding to db {e}")

################################## models ########################################


class EmployeeData(db.Model):

    emp_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    org = db.relationship("Organization", backref='employeedata', lazy=True)

    __tablename__ = "employeedata"


class Organization(db.Model):

    org_id = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, nullable=False)
    emp_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employeedata'))


if __name__ == "__main__":
    app.add_url_rule("/", view_func=InputProcessor.as_view("inputprocessor",
                                                           template_name="landing.html"))
    app.run(debug=True)
