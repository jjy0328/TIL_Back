from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # 패스워드 암호화
from flask_login import LoginManager  # 간편 로그인

app = Flask(__name__)
# 사용 할 DB URI(Uniform Resource Identifier)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost:3306/market_db'
# SECERTE KEY로 전환. terminal에서 os.urandom(12).hex()로 불러옴
app.config['SECRET_KEY'] = 'bd29b6d99fbfd2f98f411792'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from market import routes
