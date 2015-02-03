from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, template_folder='../../templates', static_folder='../../assets')
app.config.from_object('m_hero.settings')
db = SQLAlchemy(app)

app.wsgi_app = ProxyFix(app.wsgi_app)

from apps.main import views, models