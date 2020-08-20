from faker import Faker
from main import app, db, Employee, Post, Tag, tags
from sqlalchemy import func
import random

fake = Faker()

def generate_users(user_range):



    for i in range(1,user_range):
        emp = Employee()
        emp.username = fake.name()
        emp.password = "password"
        print(f" The value of i is {i}")
        #emp.id = i
        try:
            print(f" The employee being added is {emp}")
            db.session.add(emp)
            db.session.commit()
        except Exception as e:
            print(f" Error while commiting to db {e} ")


def generate_tags(no_of_tags):
    tag_list = list()
    for i in range(no_of_tags):
        tag = Tag(fake.color_name())
        try:
            tag_list.append(tag)
            db.session.add(tag)
            db.session.commit()
        except Exception as e:
            print(f" Error while adding tags {e}")
    return tag_list


def query_users():
    emp = Employee.query.order_by(Employee.id).all()
    emp_count = Employee.query.count()
    emp_count_1 = db.session.query(func.count(Employee.id)).scalar()
    for e in emp:
        print(e.id, e.username, e.password)
    emp_specfic = Employee.query.filter(Employee.id == 3).first()
    print(emp_specfic.id, emp_specfic.username)


def generate_posts(n, users, tags):
    print(tags)
    for i in range(n):
        post = Post()
        post.title = fake.sentence()
        post.text = fake.text(max_nb_chars=1000)
        post.publish_date = fake.date_this_century(before_today=True, after_today=False)
        post.emp_id = random.randrange(1, 100)
        post.tags = [tags[random.randrange(0,len(tags))] for i in range(0,2)]

        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print(f" The exception is {e}")


def query_tags():
    tag = Tag.query.filter(Tag.id >= 1).all()

    for t in tag:
        print(t.id, t.name)


def query_posts():
    post = Post.query.all()
    post_count = Post.query.count()
    print(f" The tag count is {post_count}")
    for p in post:
        print(p.emp_id, p.title, p.publish_date, p.tags)


def clean_up_model(model_name):

    db.session.query(model_name).filter(model_name.username == "Carly Allen").delete()
    db.session.commit()

#generate_users(100)
#clean_up_model(Employee)
#query_users()
#generate_tags(100)
#query_tags()

#generate_posts(10, 10, generate_tags(5))
query_posts()