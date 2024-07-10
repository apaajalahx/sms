from flask import Flask, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from .config import config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def init_app(env = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    db.init_app(app)
    csrf.init_app(app)
    app.template_folder = 'templates'
    app.static_folder = 'public'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.errorhandler(404)
    def notfound(e):
        return render_template("404.html")
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html")
    
    @app.errorhandler(500)
    def internalservererror(e):
        return render_template("500.html")
    
    @app.errorhandler(CSRFError)
    def csrferror(e):
        return render_template("csrf_error.html")

    @app.get('/robots.txt')
    def noindex():
        r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype='text/plain')
        r.headers['Content-Type'] = "text/plain; charset=utf-8"
        return r
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Users
        return Users.query.get(int(user_id))

    from src.modules.auth.views import auth
    app.register_blueprint(auth)
    
    from src.modules.dashboard.views import dashboard
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    from src.modules.contacts.views import contacts
    app.register_blueprint(contacts, url_prefix='/dashboard/contacts')

    from src.modules.template.views import template
    app.register_blueprint(template, url_prefix='/dashboard/template')

    from src.modules.setting.views import setting
    app.register_blueprint(setting, url_prefix='/dashboard/setting')
    
    from src.modules.sms.views import sms
    app.register_blueprint(sms, url_prefix='/dashboard/sms')

    return app