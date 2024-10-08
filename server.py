from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_url, UserMixin, login_user, logout_user
from distutils.log import debug 
from fileinput import filename 
from flask import * 
import importlib.util
import sys
import backtrader as bt
import yfinance as yf
# Create a flask application
app = Flask(__name__)
 
# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "abc"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy()
 
# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
 
 
# Initialize app with extension
db.init_app(app)
# Create database within app context
 
with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by 
    # filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the 
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("home"))
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    return render_template("login.html")
@app.route("/")
def home():
    # Render home.html on "/" route
    return render_template("home.html")
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)
        finalMoneyMade = runstrat(f.filename)
        return render_template("Acknowledge.html",name = f.filename)   
def load_strategy(file_path):
    spec = importlib.util.spec_from_file_location("user_strategy", file_path)
    strategy_module = importlib.util.module_from_spec(spec)
    sys.modules["user_strategy"] = strategy_module
    spec.loader.exec_module(strategy_module)
    return strategy_module.LinearRegressionStrategy

def runstrat(filename):
    strategy_file = filename
    strategy_class = load_strategy(strategy_file)

    cerebro = bt.Cerebro()

    # Add the custom strategy
    cerebro.addstrategy(strategy_class)
    
    # Download data from Yahoo Finance
    nvda_data = yf.download("NVDA", start="2018-01-01", end="2018-12-31")

    # Convert data to PandasData for backtrader
    data = bt.feeds.PandasData(dataname=nvda_data)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.addobserver(bt.observers.Value)
    prev = cerebro.broker.getvalue()
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    cerebro.plot(iplot=True, volume=False)
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')
    return cerebro.broker.getvalue()
    
if __name__ == "__main__":
    app.run()