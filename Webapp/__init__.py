from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

DB_path = "Webapp/DND5e.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DND5e.db"
app.config['SECRET_KEY'] = "suipdfnvbpoiuenvq3ono1å23neåo1i234h809sdva89k123j289340789edfvadfweor"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"




from Webapp import routes
