import requests
from flask import Flask, render_template, request, url_for, session, redirect, g
import flask_login
from funct import *

app = Flask(__name__)

app.secret_key = 'haida'

@app.route("/")
def index():
    return render_template('profile.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        form_email = request.form['emailValue']
        form_password = request.form['passwordValue']
        user = list(login_info(form_email, form_password))
        id = user[0]
        email = user[1]
        password = user[2]
        if request.form['emailValue'] == email and request.form['passwordValue'] == password:
            session['user_id'] = id
            session['user_email'] = email
            print(session['user_id'])
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html', email = session['user_email'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='127.0.0.1')
