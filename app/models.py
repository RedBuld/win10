from wtforms import Form, BooleanField, TextField, PasswordField, validators
from app import app, db
from datetime import datetime
from sqlalchemy import bindparam
import hashlib, re, random, string

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(250), index=True)
    password = db.Column('password', db.String(250))
    email = db.Column('email', db.String(100), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    locale = db.Column('locale', db.String(5))
    rank = db.Column('rank', db.Integer)

    def init(self, username, password, email, locale, rank, phone):
        self.username = username
        self.set_password(password)
        self.set_email(email)
        self.locale = locale
        self.registered_on = datetime.now()
        self.rank = rank

    def set_password(self, password):
        m = hashlib.md5()
        m.update(password)
        m = m.hexdigest()
        self.password = m[:-len(m)+250]

    def set_email(self, email):
        self.email = str(email).lower()

    def set_phone(self, phone):
        try:
            if phone[0] + phone[1] == '+7':
                phone = phone[2:]
        except Exception, e:
            pass
        phone = re.sub('[+,:;!@#$\-\/)(\n\r\s+]', '', phone)
        if len(phone) == 10:
            phone = '+7' + phone
        self.phone = phone

    def set_pos(self, coord):
        self.coord = coord
        self.coord_date = datetime.now()

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

# /*-------------------------------------------------------------------------*/

class Upload(db.Model):
    url = db.Column('url', db.String(250), index=True, unique=True, primary_key=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def init(self, url):
        self.url = url
        self.registered_on = datetime.now()