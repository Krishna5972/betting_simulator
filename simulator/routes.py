from flask import render_template,url_for, flash, redirect , request
from simulator import app,db,bcrypt
from simulator.forms import RegistrationForm, LoginForm ,NewBet
from simulator.models import User,Bets_placed
from flask_login import login_user,current_user,logout_user,login_required


@app.route('/index')
@app.route('/')
def index():
    
    return render_template('index.html',title='Index')

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
    
    

#main functionality

@app.route('/newbet',methods=['GET', 'POST'])
@login_required
def newbet():
    form = NewBet()
    if form.validate_on_submit():
        return_=form.stake.data*form.ratio.data
        new_bet=Bets_placed(team_a=form.teamA.data,team_b=form.teamB.data,condition=form.bet_condtion.data,stake=form.stake.data,
                            ratio=form.ratio.data,return_=return_,user_id=current_user.username)
        
        db.session.add(new_bet)
        db.session.commit()
        flash(f'Bet placed successfully', 'success')
        return redirect(url_for('newbet'))
    
    
    
    return render_template('newbet.html',title='New Bet',form=form)

import pandas as pd

@app.route('/openbets',methods=['GET', 'POST'])
@login_required
def openbets():
    b=Bets_placed.query.filter_by(user_id='krishna5972',bet_status='Open')
    
    dict_={}
    for i in b:
        mini_dict_={}
        mini_dict_['id']=i.id
        mini_dict_['date_placed']=i.date_placed
        mini_dict_['team_a']=i.team_a
        mini_dict_['team_b']=i.team_b
        mini_dict_['condition']=i.condition
        mini_dict_['stake']=i.stake
        mini_dict_['ratio']=i.ratio
        mini_dict_['return_']=i.return_
        mini_dict_['bet_status']=i.bet_status
        
        dict_[i.id]=mini_dict_
    bets_open_df=pd.DataFrame(dict_).transpose()

    return render_template('openbets.html',tables=[bets_open_df.to_html(classes='data')],title='Open Bets',titles=bets_open_df.columns.values)
    
    