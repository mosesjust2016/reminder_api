from flask import Flask, Response
import urllib.parse
from extensions import db, jwt
from decouple import config
from flask_cors import CORS
from datetime import datetime, timedelta
from flask_recaptcha import ReCaptcha

from .members.reminder_membership import reminder_membership

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
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mosesjasitk_Admin:'+ encoded +'@localhost/mosesjasitk_reminder'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(reminder_membership, url_prefix="/reminder_membership")

    return app