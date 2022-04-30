from flask import render_template,url_for, flash, redirect , request
from simulator import app,db,bcrypt
from simulator.forms import RegistrationForm, LoginForm ,NewBet ,Settle,Deposit,Withdraw
from simulator.models import User,Bets_placed,Transactions
from flask_login import login_user,current_user,logout_user,login_required
from datetime import datetime 
from sqlalchemy.sql import func

@app.route('/index')
@app.route('/')
def index():
    if current_user.is_authenticated:
        current_amount=User.query.filter_by(username=current_user.username).first()
        balance=current_amount.amount
        return render_template('index.html',title='Index',balance=balance)
    return render_template('index.html',title='Index')

@app.route('/about')
def about():
    if current_user.is_authenticated:
        current_amount=User.query.filter_by(username=current_user.username).first()
        balance=current_amount.amount
        return render_template('about.html',title='Index',balance=balance)
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


@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
            current_amount=User.query.filter_by(username=current_user.username).first()
            balance=current_amount.amount
    form1 = Deposit()
    form2 = Withdraw()
    if form1.validate_on_submit():
        user=User.query.filter_by(username=current_user.username).first()
        user.amount=user.amount+form1.amount.data
        user_transactions=Transactions(username=current_user.username,type='deposit',amount=form2.amount.data,date_placed=datetime.now())
        db.session.add(user_transactions)
        db.session.commit()
        flash(f'{form1.amount.data} deposited Successfully ', 'success')
        if current_user.is_authenticated:
            current_amount=User.query.filter_by(username=current_user.username).first()
            balance=current_amount.amount
        return redirect(url_for('account'))
    
    total_deposited=db.session.query(func.sum(Transactions.amount)).filter(Transactions.username==current_user.username,Transactions.type=='deposit').first()
    total_withdrawn=db.session.query(func.sum(Transactions.amount)).filter(Transactions.username==current_user.username,Transactions.type=='withdraw').first()
    try:
        net_position=balance-abs(total_deposited[0]-total_withdrawn[0])
    except TypeError:
        try:
            net_position=balance-total_deposited[0]
        except TypeError:
            net_position=0
        
        

    return render_template('account.html', title='Account',form1=form1,form2=form2,balance=balance,net_position=net_position)
    
@app.route("/account/withdraw",methods=['GET', 'POST'])
@login_required
def withdraw():
    print('hitting')
    form1 = Deposit()
    form2 = Withdraw()
    if form2.validate_on_submit():
        user=User.query.filter_by(username=current_user.username).first()
        user.amount=user.amount-form2.amount.data
        user_transactions=Transactions(username=current_user.username,type='withdraw',amount=form2.amount.data,date_placed=datetime.now())
        db.session.add(user_transactions)
        db.session.commit()
        flash(f'{form2.amount.data} Withdrawn Successfully ', 'success')
        if current_user.is_authenticated:
            current_amount=User.query.filter_by(username=current_user.username).first()
            balance=current_amount.amount
        return redirect(url_for('account'))
    
    return render_template('account.html', title='Account',form1=form1,form2=form2,balance=balance)

#main functionality

@app.route('/newbet',methods=['GET', 'POST'])
@login_required
def newbet():
    if current_user.is_authenticated:
            current_amount=User.query.filter_by(username=current_user.username).first()
            balance=current_amount.amount
    form = NewBet()
    if form.validate_on_submit():
        return_=form.stake.data*form.ratio.data
        if balance > form.stake.data:
            new_bet=Bets_placed(team_a=form.teamA.data,team_b=form.teamB.data,condition=form.bet_condtion.data,stake=form.stake.data,
                                ratio=form.ratio.data,return_=return_,username=current_user.username,date_placed=datetime.now())
            
            db.session.add(new_bet)
            current_amount=User.query.filter_by(username=current_user.username).first()
            current_amount.amount=current_amount.amount-form.stake.data
            db.session.commit()
            flash(f'Bet placed successfully', 'success')
            return redirect(url_for('newbet'))
        else:
            flash(f'Deposit money to place this bet', 'danger')
            return redirect(url_for('newbet'))
            
    
    
    
    return render_template('newbet.html',title='New Bet',form=form,balance=balance)

@app.route('/openbets',methods=['GET', 'POST'])
@login_required
def openbets():
    if current_user.is_authenticated:
            current_amount=User.query.filter_by(username=current_user.username).first()
            balance=current_amount.amount
    bets=Bets_placed.query.filter_by(username=current_user.username,bet_status='Open')
    form = Settle()
    # dict_={}
    # for i in qinter:
    #     mini_dict_={}
    #     mini_dict_['id']=i.id
    #     mini_dict_['date_placed']=(i.date_placed).strftime("%d/%m/%Y, %H:%M")
    #     mini_dict_['team_a']=i.team_a
    #     mini_dict_['team_b']=i.team_b
    #     mini_dict_['condition']=i.condition
    #     mini_dict_['stake']=i.stake
    #     mini_dict_['ratio']=i.ratio
    #     mini_dict_['return_']=i.return_
    #     mini_dict_['bet_status']=i.bet_status
        
    #     dict_[i.id]=mini_dict_
    # bets_open_df=pd.DataFrame(dict_).transpose()
    
    if form.validate_on_submit():
        bet_id = request.form.get('bet_id')
        if form.state.data=='Won':
            bet=Bets_placed.query.filter_by(bet_id=bet_id).first()
            bet.bet_status = 'Won'
            current_amount=User.query.filter_by(username=current_user.username).first()
            current_amount.amount=current_amount.amount+bet.return_
            db.session.commit()
            
        elif form.state.data=='Lost':
            bet=Bets_placed.query.filter_by(bet_id=bet_id).first()
            bet.return_=0
            bet.bet_status = 'Lost'
            db.session.commit()
            
        else:
            bet=Bets_placed.query.filter_by(bet_id=bet_id).first()
            bet.bet_status = 'Void'
            current_amount=User.query.filter_by(username=current_user.username).first()
            bet.return_=0
            current_amount.amount=current_amount.amount+bet.stake
            db.session.commit()
        flash(f'Selected Bet Closed successfully', 'success')
        return redirect(url_for('openbets'))
    return render_template('openbets.html',bets=bets,form=form,balance=balance)


@app.route('/bet_history',methods=['GET', 'POST'])
@login_required
def bet_history():
    if current_user.is_authenticated:
            current_amount=User.query.filter_by(username=current_user.username).first()
            balance=current_amount.amount

    
    bets=Bets_placed.query.filter(Bets_placed.bet_status !='Open',Bets_placed.username==current_user.username)
    
    return render_template('bets_history.html',bets=bets,balance=balance)