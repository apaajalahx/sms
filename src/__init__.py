from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config

db = SQLAlchemy()
login_manager = LoginManager()
def init_app(env = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    app.template_folder = 'templates'
    app.static_folder = 'public'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import Users
        return Users.query.get(int(user_id))
    
    from src.modules.auth.views import auth
    app.register_blueprint(auth)
    
    
    return app