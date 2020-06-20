from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, current_user 
from werkzeug.security import check_password_hash

from chaos.extensions import db 
from chaos.models import User 
from datetime import datetime 
import pytz 

auth = Blueprint('auth', __name__)

def user_already_exists(email):
    users = User.query.all()
    for user in users:
        if user.email == email:
            return True 
    return False 

@auth.route('/admin_login', methods = ['GET','POST'])
def admin_login():
    admins = User.query.all()
    error = status = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = None 
        for x in admins:
            if x.email == email:
                admin = x 
                break
        
        if not admin or not check_password_hash(admin.password, password):
            error = 'Invalid credentials'
        elif admin.is_admin:
            flash('You were successfully logged in', "message")
            login_user(admin)
            if current_user.start_time == None:
                dt = datetime.now(tz=pytz.UTC)
                current_user.start_time = dt.astimezone(pytz.timezone('Asia/kolkata'))
                db.session.commit()
        else:
            error = 'you are not an admin'
        return render_template('admin_login.html', error = error)
    return render_template('admin_login.html', error=error)



@auth.route('/admin_olagebaa', methods = ['GET','POST'])
def admin_register():
    error = ''
    if request.method == 'POST':
        name = request.form['name']
        unhashed_passwd = request.form['password']
        unhashed_confirm_passwd = request.form['confirm_password']
        email = request.form['email']
        phone = request.form['phone']
        if unhashed_passwd != unhashed_passwd:
            error = 'passwords does not match'
        elif user_already_exists(email):
            error = 'user already exists'
        else:
            user = User(name=name, email=email, unhashed_password=unhashed_passwd, phone=phone, is_admin=True, attempts='', present_try=0, nextq=1, hint=-1, score=0)
            db.session.add(user)
            db.session.commit()
            flash("Registration Successful","message")
            return redirect(url_for('auth.admin_login'))

    return render_template('admin_register.html',error=error)


@auth.route('/olagebaa', methods=['GET','POST'])
def register():
    error = ''
    if request.method=='POST':
        name = request.form['name']
        unhashed_passwd = request.form['password']
        unhashed_confirm_passwd = request.form['confirm_password']
        email = request.form['email']
        phone = request.form['phone']
        if unhashed_passwd != unhashed_confirm_passwd:
            error = 'passwords does not match'
        elif user_already_exists(email):
            error = 'user already exists'
        else:
            user = User(name=name, email=email, unhashed_password=unhashed_passwd, phone=phone, is_admin=False, attempts='', present_try=0, nextq=1, hint=-1, score=0)
            db.session.add(user)
            db.session.commit()
            flash("Registration Successful", "message")
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', error=error)

@auth.route('/login', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            error = 'Invalid credentials'
        
        if not error:
            login_user(user)    
            flash("you are successfully logged in", "message")
            if current_user.start_time == None:
                dt = datetime.now(tz=pytz.UTC)           
                current_user.start_time = dt.astimezone(pytz.timezone('Asia/Kolkata'))
                db.session.commit()
            return redirect(url_for('main.instructions'))

    return render_template('login.html', error=error)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/admin_logout')
def admin_logout():
    logout_user()
    return redirect(url_for('main.home'))
