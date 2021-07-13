from application import app, db
from application.models import Users

@app.route('/')
@app.route('/home')
def home():
    return '<h1>**** Welcome to NFL Fantasy! This is the home page. ***</h1>'

@app.route('/about')
def about():
    return '<h1>*** This is the about page ***</h1>'

@app.route('/user/<user>')
def username(user):
    if user == 'Ollie':
        return redirect(url_for('home'))
    else:
        return f'<h1>Hi, {user}! What is up bro?</h1>'

@app.route('/add/<taskname>')
def add(taskname):
    new_task = Tasks(name = taskname)
    db.session.add(new_task)
    db.session.commit()
    return "<h1>Added new task to database</h1>"

@app.route('/read')
def read():
    all_tasks = Tasks.query.all()
    tasks_string = ""
    for tasks in all_tasks:
        tasks_string += "<br>"+ str(tasks.id) + ". " + tasks.name
    return f'<h1>{tasks_string}</h1>'

@app.route('/update/<description>')
def update(description):
    first_task = Tasks.query.first()
    first_task.description = description
    db.session.commit()
    return f'<h1>{first_task.description}</h1>'

@app.route('/delete')
def delete():
    task_to_delete = Tasks.query.first()
    db.session.delete(task_to_delete)
    db.session.commit()
    return "<h1>Task deleted!</h1>"

@app.route('/count')
def count():
    num_tasks = Tasks.query.count()
    return f'<h1>Number of tasks: {num_tasks}</h1>'

@app.route('/completed/<bool>')
def completed(bool):
    completed_task = Tasks.query.first()
    if bool == 'True':
        completed_task.completed = True
        db.session.commit()
        return f'<h1><b>{completed_task.name}</b> has been completed!</h1>'
    elif bool == 'False':
        completed_task.completed = False
        db.session.commit()
        return f'<h1><b>{completed_task.name}</b> has not been completed yet!</h1>'