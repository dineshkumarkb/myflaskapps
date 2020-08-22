from flask import Flask, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, DataRequired, Email, email_validator

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(DevConfig)


@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')


class Restaurant(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Restaurant {self.name}, {self.id}"


class CommentForm(FlaskForm):
    author = StringField('author', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])


@app.route("/submit", methods=['GET', 'POST'])
def get_form():
    form = CommentForm()
    print(f" Received form data {form}")
    if form.validate_on_submit():
        print(f" Form validated ")
        print(f" Form data received {form.author.data}, {form.email.data}", 'info')
        flash(f" Form data received {form.author.data}, {form.email.data}", 'info')
        return redirect(url_for('get_form'))
    return render_template('submit.html', form=form)


if __name__ == "__main__":
    app.run()

