from flask import Flask, Response
import urllib.parse
from extensions import db, jwt
from decouple import config
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_recaptcha import ReCaptcha

from .members.reminder_membership import reminder_membership
from .members.account_management import account_management
from .members.member_profile import member_profile
def create_app():
    app = Flask(__name__)
    CORS(app)
    recaptcha = ReCaptcha(app)

    app.config['RECAPTCHA_SITE_KEY'] = 'YOUR_RECAPTCHA_SITE_KEY'
    app.config['RECAPTCHA_SECRET_KEY'] = 'YOUR_RECAPTCHA_SECRET_KEY'

    app.config['PROPAGATE_EXCEPTIONS'] = True

    db_enviroment  = config('ENVIROMENT')
    db_password = config('DB_PASS')

    if db_enviroment == "Development":
        encoded = urllib.parse.quote_plus(db_password)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:'+ encoded +'@localhost/mosesjasitk_reminder'

    else:
        encoded = urllib.parse.quote_plus(db_password)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mosesjasi_Admin:'+ encoded +'@localhost/mosesjasi_reminder'

    
     #JWT configs
    app.secret_key = config('SECRET_KEY')  
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=6)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config["JWT_ALGORITHM"] = "HS256"
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(reminder_membership, url_prefix="/reminder_membership")
    app.register_blueprint(account_management, url_prefix="/account_management")
    app.register_blueprint(member_profile, url_prefix="/member_profile")

    return app