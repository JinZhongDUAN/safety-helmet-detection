from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = '你必须登录才能进入这个页面'
login.login_message_category = 'info'


from app import views