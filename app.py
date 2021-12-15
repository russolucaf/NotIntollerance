from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_session import Session
from RestaurantForm import RestaurantForm
from SignUpForm import SignUp
from SignInForm import SignInForm
from mongoengine import *
from User import User
from Restaurant import Restaurant
from flask_bcrypt import Bcrypt
from datetime import timedelta
import secrets

app = Flask(__name__)

bcrypt = Bcrypt(app)
# app.config['SECRET_KEY'] = '4599b8b8c2a893fc8b453da9'

app.secret_key = secrets.token_urlsafe(32)
app.config['SESSION_TYPE'] = 'mongodb'

Session(app)

connect('admin')


@app.route("/")
def index():
    if 'user_profile' in session:
        return render_template('index.html', name=index)
    else:
        return render_template('index.html', name=index)


@app.route('/sign_up', methods=['POST', 'GET'])
def login_sign_up():
    if 'user_profile' in session:
        return redirect(url_for('index'))
    form = SignUp()
    if request.method == "GET":
        return render_template('sign_up.html', form=form)
    else:
        users = User()
        users.name = request.form.get('name').lower()
        users.surname = request.form.get('surname').lower()
        users.email = request.form.get('email').lower()
        password = request.form.get('password')
        if (len(password) <= 8) or (len(password) >= 20):
            flash("Attenzione, password troppo lunga o corta!")
            return redirect(url_for('login_sign_up'))
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        users.password = password_hash
        for user in User.objects(email=users.email):
            if user.email == users.email:
                flash("Email già esistente!")
                return redirect(url_for('login_sign_up'))
        else:
            users.save()
            session['user_profile'] = users.email
            redirect(url_for('index'))
    return redirect(url_for('login_sign_up'))


@app.route('/logout')
def login_exit():
    session.pop('user_profile', None)
    return redirect(url_for('index'))


@app.route('/sign_in', methods=['POST', 'GET'])
def login_sign_in():
    form = SignInForm()
    if 'user_profile' in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template('sign_in.html', form=form)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        for users in User.objects(email=email):
            if users.email == email and bcrypt.check_password_hash(users.password, password):
                session['user_profile'] = users.email
                return redirect(url_for('index'))
        else:
            flash("Email o password non validi!")
            redirect(url_for('login_sign_in'))
    return render_template('sign_in.html', form=form)


@app.route('/restaurant_view')
def restaurant_view():
    rest_objects = []
    for rest in Restaurant.objects:
        rest_objects.append(Restaurant(rest.partita_iva,
                                       rest.name,
                                       rest.address,
                                       rest.civic_number,
                                       rest.cap,
                                       rest.city,
                                       rest.email,
                                       rest.number_phone))
    return render_template('restaurant_view.html', rest_objects=rest_objects)


@app.route('/restaurant_register', methods=["GET", "POST"])
def restaurant():
    form = RestaurantForm()
    if request.method == "GET":
        return render_template('restaurant_form.html', form=form)
    else:
        restaurants = Restaurant(request.form.get('partita_iva'),
                                 request.form.get('name'),
                                 request.form.get('address'),
                                 request.form.get('civic_number'),
                                 request.form.get('cap'),
                                 request.form.get('city'),
                                 request.form.get('email').lower(),
                                 request.form.get('number_phone'))
        if restaurants.email is None:
            flash("Errore")
            return redirect(url_for('restaurant'))
        for rest in Restaurant.objects(email=restaurants.email):
            if restaurants.email == rest.email:
                flash("Email o partita iva già esistente!")
                return redirect(url_for('restaurant'))
        for rest in Restaurant.objects(partita_iva=restaurants.partita_iva):
            if restaurants.partita_iva == rest.partita_iva:
                flash("Email o partita iva già esistente!")
                return redirect(url_for('restaurant'))
        else:
            restaurants.save()
            flash('Registrazione in fase di accettazione!')
            return redirect(url_for('restaurant'))


@app.route('/search_restaurant', methods=["POST", "GET"])
def restaurant_search():
    rest_objects = []
    if request.method == "POST":
        search = request.form.get('search_form').lower()
        for rest in Restaurant.objects():
            if search in rest.name.lower():
                rest_objects.append(Restaurant(rest.partita_iva,
                                               rest.name,
                                               rest.address,
                                               rest.civic_number,
                                               rest.cap,
                                               rest.city,
                                               rest.email,
                                               rest.number_phone))
                return render_template('restaurant_view.html', rest_objects=rest_objects)
        else:
            flash("Non esiste nessun ristorante con questo nome")
            return redirect(url_for('restaurant_view'))


if __name__ == '__main__':
    app.run()
