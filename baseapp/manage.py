from main import app, db, Employee




@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Employee=Employee)