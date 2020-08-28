from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, Length, email_validator, InputRequired
from wtforms.fields.html5 import EmailField
from config import DevConfig

app = Flask(__name__)
db = app.config.from_object(DevConfig)


class UserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    email = EmailField('email', validators=[Email()])


@app.route("/index", methods=['GET', 'POST'])
def index():
    user_form = UserForm()
    print(request.method)
    if request.method == "POST":
        print(f" POST request received ")
        if user_form.validate_on_submit():
            name = user_form.username.data
            email = user_form.email.data
            password = user_form.password
            print(f" User form validated {name}, {email}")
            return redirect(url_for('index'))

    return render_template('index.html', form=user_form)


@app.route("/", methods=['GET', 'POST'])
def landing():
    print("Landing")
    myform = UserForm()
    if request.method == 'POST':
        if myform.validate_on_submit():
            print(f" Form validated ")
            return redirect(url_for('landing'))

    return render_template('helpers.html', form=myform)


if __name__ == "__main__":
    app.run()