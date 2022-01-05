from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_session import Session
from flask_mongoengine import MongoEngine

from RestaurantApprove import RestaurantApprove
from RestaurantForm import RestaurantForm
from Review import Review
from ReviewForm import ReviewForm
from SignUpForm import SignUp
from SignInForm import SignInForm
from mongoengine import *
from User import User
from Restaurant import Restaurant
from flask_bcrypt import Bcrypt
import pymongo
from datetime import timedelta
import secrets
import time

app = Flask(__name__)

bcrypt = Bcrypt(app)
# app.config['SECRET_KEY'] = '4599b8b8c2a893fc8b453da9'

app.secret_key = secrets.token_urlsafe(32)
app.config['SESSION_TYPE'] = 'mongodb'
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = myclient['admin']
my_collection = my_db['user']
Session(app)

connect('admin')


@app.before_request
def session_lifetime():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


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
            session['user_name'] = users.name
            return redirect(url_for('index'))


@app.route('/logout')
def login_exit():
    session.pop('user_profile', None)
    session.pop('admin', None)
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
        if email == "lukaein@admin.it" and password == "lukaein99":
            session['admin'] = email
            return redirect(url_for('index'))
        for users in User.objects(email=email):
            if users.email == email and bcrypt.check_password_hash(users.password, password):
                session['user_profile'] = users.email
                session['user_name'] = users.name
                return redirect(url_for('index'))
        else:
            flash("Email o password non validi!")
            redirect(url_for('login_sign_in'))
    return render_template('sign_in.html', form=form)


@app.route('/restaurant_view')
def restaurant_view():
    rest_objects = []
    for rest in Restaurant.objects:
        rest_objects.append(Restaurant(
                                       id=rest.id,
                                       partita_iva=rest.partita_iva,
                                       name=rest.name,
                                       address=rest.address,
                                       civic_number=rest.civic_number,
                                       cap=rest.cap,
                                       city=rest.city,
                                       email=rest.email,
                                       url_img=rest.url_img,
                                       number_phone=rest.number_phone))
    return render_template('restaurant_view.html', rest_objects=rest_objects)


@app.route('/delete_review/<review_id>', methods=['POST'])
def delete_review(review_id):
    if 'admin' in session:
        for review in Review.objects(id=review_id):
            email = review.restaurant_email
            if review_id:
                review.delete()
                return redirect(url_for('restaurant_specific', rest_object=email))
    return redirect(url_for('delete_review', review_id=review_id))


@app.route('/restaurant_specific/<rest_object>', methods=['POST', 'GET'])
def restaurant_specific(rest_object):
    form_review = ReviewForm()

    if request.form.get('body') == "" or request.form.get('body') == " ":
        flash("Scrivi almeno qualcosa all'interno della recensione!")
        return redirect(url_for('restaurant_view'))
    if form_review.validate_on_submit():
        review = Review(user_email=session['user_profile'],
                        restaurant_email=rest_object,
                        body=request.form.get('body'))
        review.save()

    review_objects = []
    for rew in Review.objects(restaurant_email=rest_object):
        review_objects.append(Review(
                                     id=rew.id,
                                     user_email=rew.user_email,
                                     restaurant_email=rew.restaurant_email,
                                     body=rew.body))
    for rest in Restaurant.objects(email=rest_object):
        if rest.email == rest_object:
            return render_template('restaurant_specific.html', rest=rest, form=form_review, rew=review_objects)

    return redirect(url_for('restaurant_specific', rest_object=rest_object))


@app.route('/restaurant_register', methods=["GET", "POST"])
def restaurant():
    form = RestaurantForm()
    if request.method == "GET":
        return render_template('restaurant_form.html', form=form)
    else:
        restaurants = RestaurantApprove(request.form.get('partita_iva'),
                                        request.form.get('name'),
                                        request.form.get('address'),
                                        request.form.get('civic_number'),
                                        request.form.get('cap'),
                                        request.form.get('city'),
                                        request.form.get('email').lower(),
                                        request.form.get('url_img'),
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


# ADMIN PANEL
@app.route('/admin_panel')
def admin_panel():
    rest = []
    for risto in RestaurantApprove.objects:
        rest.append(RestaurantApprove(
                                   id=risto.id,
                                   partita_iva=risto.partita_iva,
                                   name=risto.name,
                                   address=risto.address,
                                   civic_number=risto.civic_number,
                                   cap=risto.cap,
                                   city=risto.city,
                                   email=risto.email,
                                   url_img=risto.url_img,
                                   number_phone=risto.number_phone)
        )
    return render_template('admin_panel.html', rest=rest)


@app.route('/approve_restaurant/<resto_id>', methods=['POST', 'GET'])
def approve_restaurant(resto_id):
    if 'admin' in session:
        if resto_id:
            for approve_resto in RestaurantApprove.objects(id=resto_id):
                restaurants = Restaurant(
                    approve_resto.partita_iva,
                    approve_resto.name,
                    approve_resto.address,
                    approve_resto.civic_number,
                    approve_resto.cap,
                    approve_resto.city,
                    approve_resto.email,
                    approve_resto.url_img,
                    approve_resto.number_phone
                )
                restaurants.save()
            restaurant_delete = RestaurantApprove.objects(id=resto_id)
            restaurant_delete.delete()

    return redirect(url_for('admin_panel'))


@app.route('/delete_restaurant/<resto_id>', methods=['POST', 'GET'])
def delete_restaurant(resto_id):
    if 'admin' in session:
        if resto_id:
            restaurant_delete = RestaurantApprove.objects(id=resto_id)
            restaurant_delete.delete()

    return redirect(url_for('admin_panel'))


@app.route('/delete_from_restaurants/<resto_id>', methods=['POST', 'GET'])
def delete_from_restaurants(resto_id):
    if 'admin' in session:
        if resto_id:
            restaurant_delete = Restaurant.objects(id=resto_id)
            restaurant_delete.delete()

    return redirect(url_for('restaurant_view'))


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
                                               rest.url_img,
                                               rest.number_phone))
                return render_template('restaurant_view.html', rest_objects=rest_objects)
        else:
            flash("Non esiste nessun ristorante con questo nome")
            return redirect(url_for('restaurant_view'))


@app.route('/user_profile', methods=["POST", "GET"])
def user_profile():
    form = SignInForm()
    if 'user_profile' in session:
        if request.method == "POST":
            new_password = request.form.get('password')
            if (len(new_password) <= 8) or (len(new_password) >= 20):
                flash("Attenzione, password troppo lunga o corta!")
                return redirect(url_for('user_profile'))
            else:
                new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                for users in User.objects():
                    if users.email == session['user_profile']:
                        old_password = {'password': users.password}
                        nuova_password = {'$set': {'password': new_password}}
                        my_collection.update_one(old_password, nuova_password)
                        flash('Password cambiata!')
                        return redirect(url_for('user_profile'))
    else:
        return redirect(url_for('index'))
    return render_template('user_profile.html', form=form)


if __name__ == '__main__':
    app.run()
