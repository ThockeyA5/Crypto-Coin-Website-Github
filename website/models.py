from . import db
from flask_login import UserMixin
import datetime
from datetime import datetime, timezone, timedelta

class Coins(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    CoinHistory = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone = True), default = datetime.now(timezone(timedelta(hours=-5), 'EST')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(200), unique = True)
    fullname = db.Column(db.String(200))
    Username = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200))
    CoinNum = db.Column(db.Integer)
    CoinsHistory = db.relationship('Coins')