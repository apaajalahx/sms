from . import auth
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from src.models import Users
from flask_login import login_user, login_required, logout_user, current_user


@auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('auth/login.html')


@auth.post("/login")
def loginprocess():

    username = request.form.get("username")
    password = request.form.get("password")

    if username is None or password is None:
        flash('Please check your login detail and try again.')
        return redirect(url_for('auth.login'))

    user = Users.query.filter(Users.username == username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login detail and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=False)

    return redirect(url_for('dashboard.panel'))


@auth.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))