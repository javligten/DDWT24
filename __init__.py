from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/movies.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["JWT_SECRET_KEY"] = "supersecretkey"

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
jwt = JWTManager(app)
api = Api(app)

login_manager.login_view = 'login'

# Import models
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes
from app import routes, api_routes
