from flask import Flask, render_template, url_for, redirect
from flask.views import View
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, UUID, Length, Email
from wtforms.fields.html5 import EmailField
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity, get_current_user
import uuid


app = Flask(__name__)
app.config.from_object(DevConfig())
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


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
            print(f" Received emp data {emp_id}, {name}, {email}, {encrypted_password}")
            return redirect(self.template_name)
        else:
            print(f" Invalid form { emp_form.errors }")
        return render_template(self.template_name, form=emp_form)


if __name__ == "__main__":
    app.add_url_rule("/", view_func=InputProcessor.as_view("inputprocessor",
                                                           template_name="landing.html"))
    app.run(debug=True)
