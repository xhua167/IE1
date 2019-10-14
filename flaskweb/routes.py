from flask import render_template, url_for, flash, redirect, request
from flaskweb import app, db, bcrypt
from flaskweb.forms import RegistrationForm, LoginForm
from flaskweb.getData import getServices, getInfo
from flask_login import login_user, current_user, logout_user, login_required
from flaskweb.models import User


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html', title='About us')

@app.route('/services/')
def services():
    return render_template('services.html', title='Service')

@app.route('/services/<string:service_name>')
def serviceDisplay(service_name):
    data = getServices(service_name)
    return render_template('serviceDisplay.html', title='Service Display',
                           data=data, service_name=service_name)

@app.route('/services/serviceDisplay/detailedInfo/<string:servicename>/<string:service_id>')
def detailedInfo(servicename, service_id):
    data = getInfo(servicename, service_id)
    return render_template('detailedInfo.html', title='Service Imformation',
                           data=data, servicename=servicename)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        userjson = {'username': form.username.data, 'email':form.email.data,
                'password': hashed_pw}
        collection = db.user
        collection.insert_one(userjson)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        userjson = db.user.find_one({'email': form.email.data})
        if userjson and bcrypt.check_password_hash(userjson['password'], form.password.data):
            user = User(email=userjson['email'])
            login_user(user, remember=form.remenber.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password:)', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account/")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/search/")
def search():
    return render_template('account.html', title='Account')
