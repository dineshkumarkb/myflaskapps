from main import db, Employee, app, Post, Comment, Tag, migrate


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app, Employee=Employee, Post=Post, Comment=Comment, Tag=Tag, migrate=migrate)



