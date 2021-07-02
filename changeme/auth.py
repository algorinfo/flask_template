# From https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, current_user, logout_user
from changeme import db
from changeme.models.users import User

auth = Blueprint('auth', __name__,
                 template_folder='templates/auth')


@auth.route('/login')
def login():
    """ login """
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = db.flask.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Please check your credentials")
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/signup')
def signup():
    """ signup """
    return render_template("signup.html")


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    # name = request.form.get('name')
    password = request.form.get('password')

    user = db.flask.query(User).filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, password=password)

    # add the new user to the database
    db.flask.add(new_user)
    db.flask.commit()

    return redirect(url_for('auth.login'))


@auth.route('/profile')
@login_required
def profile():
    """ signup """
    return render_template("profile.html", mail=current_user.email)


@auth.route('/logout')
def logout():
    """ logout """
    logout_user()
    return redirect(url_for('root.hello'))
