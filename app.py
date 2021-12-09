from flask import Flask, render_template, redirect, url_for, request, flash
from SignUpForm import SignUp
from SignInForm import SignInForm
from flask_mongoengine import MongoEngine
from mongoengine import *
from User import User
from passlib.context import CryptContext
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '4599b8b8c2a893fc8b453da9'

connect('admin')


@app.route("/")
def index():
    return render_template('index.html', name=index)


@app.route('/sign_up', methods=['POST', 'GET'])
def login_sign_up():
    form = SignUp()
    if request.method == "GET":
        return render_template('sign_up.html', form=form)
    else:
        users = User()
        users.name = request.form.get('name')
        users.surname = request.form.get('surname')
        users.email = request.form.get('email')
        password = request.form.get('password')
        if (len(password) <= 8) or (len(password) >= 20):
            flash("Attenzione, password troppo lunga o corta!")
            return redirect(url_for('login_sign_up'))
        users.password = password
        for user in User.objects(email=users.email):
            if user.email == users.email:
                flash("Email già esistente!")
                return redirect(url_for('login_sign_up'))
        else:
            users.save()
            flash("Registrazione avvenuta con successo!")
    return redirect(url_for('login_sign_up'))


@app.route('/sign_in', methods=['POST', 'GET'])
def login_sign_in():
    form = SignInForm()
    if request.method == "GET":
        return render_template('sign_in.html', form=form)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        for users in User.objects(email=email, password=password):
            if users.email == email and users.password == password:
                flash("Benvenuto " + users.name + "!")
                return redirect(url_for('index'))
        else:
            flash("Email o password non validi!")
    return render_template('sign_in.html', form=form)


if __name__ == '__main__':
    app.run()
