from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'testingSecretKey123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize database
    db.init_app(app)

    # initialize login manager
    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    from models import User, Assignment, Answer
    @loginManager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    # setup auth blueprint
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    # setup main blueprint
    from main import main as main_bp
    app.register_blueprint(main_bp)
    return app