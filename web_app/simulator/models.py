from datetime import datetime
from simulator import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)
    bets = db.relationship('Bets_placed', backref='bets', lazy=True)
    amount=db.Column(db.Float(30) , default=0.0)

    def __repr__(self):
        return f"User('{self.username}')"

class Bets_placed(db.Model):
    bet_id = db.Column(db.Integer, primary_key=True)
    team_a = db.Column(db.String(100), nullable=False)
    team_b = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    date_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stake = db.Column(db.Float(30), nullable=False)
    ratio = db.Column(db.Float(30), nullable=False)
    return_ = db.Column(db.Float(30), nullable=False)
    bet_status = db.Column(db.String(5), default='Open')
    username = db.Column(db.String(70), db.ForeignKey('user.username'), nullable=False)
    def __repr__(self):
        return f"Post('{self.id}', '{self.ratio}')"
    
    
class Transactions(db.Model):
    transaction_id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(70), db.ForeignKey('user.username'))
    type=db.Column(db.String(10), nullable=False)
    date_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float(30), nullable=False)
 
    def __repr__(self):
        return f"Post('{self.id}', '{self.amount}')"