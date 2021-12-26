from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Coins
from . import db
import random

def CodeChange():
    a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    c = ''
    for x in range(4):
        b = random.choice(a)
        c = c + b
    file = open('website/codefiles/CodeCC.txt', 'w')
    file.write(str(c))
    file.close()

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user = current_user, CryptoPrice = open("codefiles/Price.CC.txt").read())

@views.route('/mine', methods=['GET', 'POST'])
@login_required
def mine():
    if request.method == 'POST':
        code = request.form.get('code')
        CryptoCode = open("codefiles/CodeCC.txt").read()
        if code == CryptoCode:
            mining_history = Coins(CoinHistory='Mined a CryptoCoin', user_id = current_user.id)
            db.session.add(mining_history)
            updateCoins = User.query.filter_by(id = current_user.id).first()
            updateCoins.CoinNum = User.CoinNum + 1
            db.session.commit()
            flash('Correct Code! You mined a CryptoCoin', category = 'success')
            CodeChange()
            CryptoCode = open("website/codefiles/CodeCC.txt").read()
            return redirect(url_for('views.home'))
        else:
            flash('Code is Wrong! Try Again', category = 'error')

    return render_template("mine.html", user = current_user)

@views.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    if request.method == 'POST':
      buy = request.form.get('buy')
      buy = str(buy)
      if not buy.isdigit():
          flash("Input must be a whole positive number", category = 'error')
      else:
          if int(buy) < 1:
              flash("Input must be at least 1", category = 'error')
          else:
              CryptoPrice = open("codefiles/Price.CC.txt").read()
              bought = Coins(CoinHistory='Bought ' + buy + ' CryptoCoin for $' + CryptoPrice, user_id = current_user.id)
              db.session.add(bought)
              updateCoins = User.query.filter_by(id = current_user.id).first()
              updateCoins.CoinNum = User.CoinNum + int(buy)
              db.session.commit()
              flash("CryptoCoins successfully bought!", category = 'success')
              return redirect(url_for('views.home'))
    return render_template("buy.html", user = current_user)

@views.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        sell = request.form.get('sell')
        sell = str(sell)
        updateCoins = User.query.filter_by(id = current_user.id).first()
        if not sell.isdigit():
          flash("Input must be a whole positive number", category = 'error')
        else:
            if int(sell) < 1:
                flash("Input must be at least 1", category = 'error')
            elif int(sell) > updateCoins.CoinNum:
                flash('You don\'t have enough CryptoCoin!', category = 'error')
            else:
                CryptoPrice = open("codefiles/Price.CC.txt").read()
                sold = Coins(CoinHistory='Sold ' + sell + ' CryptoCoin for $' + CryptoPrice, user_id = current_user.id)
                db.session.add(sold)
                updateCoins = User.query.filter_by(id = current_user.id).first()
                updateCoins.CoinNum = User.CoinNum - int(sell)
                db.session.commit()
                flash("CryptoCoins successfully sold!", category = 'success')
                return redirect(url_for('views.home'))
    return render_template("sell.html", user = current_user)
