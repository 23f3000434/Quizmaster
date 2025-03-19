from flask import Flask;
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager;
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='./templates', static_folder='./static')


app.config['SECRET_KEY'] = '136a09f046d522db434c3251af540eee8dc840e904195344'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from quizmaster import routes
from quizmaster.commands import create_admin, init_db_command

app.cli.add_command(create_admin)
app.cli.add_command(init_db_command)

with app.app_context():
    db.create_all()

