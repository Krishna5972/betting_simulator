from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,FloatField,RadioField
from wtforms.validators import DataRequired, Length, EqualTo,ValidationError
from simulator.models import User





class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('Username is taken')
        
        
    


class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class NewBet(FlaskForm):
    teamA = StringField('Team A',
                        validators=[DataRequired(), Length(min=2, max=20)])
    teamB = StringField('Team B',
                        validators=[DataRequired(), Length(min=2, max=20)])
    bet_condtion = StringField('Bet Condition',
                        validators=[DataRequired()])
    stake = FloatField('Stake',
                        validators=[DataRequired()])
    ratio=FloatField('Ratio',
                        validators=[DataRequired()])
    
    submit = SubmitField('Place Bet')
    

    
    
class Settle(FlaskForm) :
    state = RadioField('BetStatus', choices=[('Won','Won'),('Lost','Lost'),('Cancel','Cancel')])
    submit = SubmitField('Settle')
    cancel = SubmitField('Cancel')
    
    

class Deposit(FlaskForm) :
    amount=FloatField('Amount',
                        validators=[DataRequired()])
    submit = SubmitField('Deposit')
    
class Withdraw(FlaskForm) :
    amount=FloatField('Amount',
                        validators=[DataRequired()])
    submit = SubmitField('Withdraw')