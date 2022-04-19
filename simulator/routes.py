from flask import render_template,url_for, flash, redirect , request
from simulator import app,db,bcrypt
from simulator.forms import RegistrationForm, LoginForm
from simulator.models import User,Bets_placed
from flask_login import login_user,current_user,logout_user,login_required

open_bet_ids=[1,2,3,4]

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html',open_bet_ids=open_bet_ids,title='Index')

@app.route('/about')
def about():
    return render_template('about.html',title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
             
            return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
    