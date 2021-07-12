from flask import Flask
from flask import redirect
from flask import url_for

app2 = Flask(__name__)

@app2.route('/')
@app2.route('/home')

def home():
    return '<h1>**** Welcome to NFL Fantasy! This is the home page. ***</h1>'

@app2.route('/about')
def about():
    return '<h1>*** This is the about page ***</h1>'

@app2.route('/user/<user>')
def username(user):
    if user == 'Ollie':
        return redirect(url_for('home'))
    else:
        return f'<h1>Hi, {user}! What is up bro?</h1>'

if __name__ == '__main__':
    app2.run(debug = True, host = '0.0.0.0')