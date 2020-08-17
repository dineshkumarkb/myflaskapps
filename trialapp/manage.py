from main import app, db, Restaurant


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app, Restaurant=Restaurant)

