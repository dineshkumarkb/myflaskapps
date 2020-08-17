from main import db, Employee, app, Post


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,app=app,Employee=Employee, Post=Post)



