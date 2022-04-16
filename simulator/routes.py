from flask import render_template,url_for, flash, redirect
from simulator.forms import RegistrationForm, LoginForm
from simulator.models import User,Bets_placed
from simulator import app

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'krishna5972' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


