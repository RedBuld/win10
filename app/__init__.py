# -*- coding: utf-8 -*
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_babelex import Babel
from flask_thumbnails import Thumbnail
from werkzeug.routing import BaseConverter
from flask_gears import Gears
from gears_stylus import StylusCompiler
from gears_less import LESSCompiler
from gears_coffeescript import CoffeeScriptCompiler
from gears_sass import SASSCompiler
from gears_clean_css import CleanCSSCompressor
from gears_uglifyjs import UglifyJSCompressor

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_SETTINGS_MODULE', 'app.settings.development'))

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

gears = Gears(
    compilers={
        '.styl': StylusCompiler.as_handler(),
        '.less': LESSCompiler.as_handler(),
        '.coffee': CoffeeScriptCompiler.as_handler(),
        '.sass': SASSCompiler.as_handler(),
        '.scss': SASSCompiler.as_handler()
    },
    compressors={
        'text/css': CleanCSSCompressor.as_handler(),
        'text/javascript': UglifyJSCompressor.as_handler()
    },
)
gears.init_app(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
babel = Babel(app)
thumb = Thumbnail(app)


from app import models, views
from models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
