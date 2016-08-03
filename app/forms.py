from flask_babelex import lazy_gettext, gettext as _, ngettext
from app import app, db, babel
from wtforms import TextAreaField, ValidationError, Form, BooleanField, IntegerField, TextField, PasswordField, SelectField, validators
from flask_wtf.file import FileAllowed, FileRequired, FileField
from flask_wtf import Form, RecaptchaField
import hashlib
from flask_login import current_user
from app.models import User
from app.tools import remove_img, check_img, remove_icon, check_icon

class LoginForm(Form):
    email = TextField('Email', [
        validators.Length(min=4, max=50),
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Length(max=250),
        validators.Required()
    ])
    remember_me = BooleanField(u'remember_me')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.email.label.text = _(u'Email')
        self.password.label.text = _(u'Password')
        self.remember_me.label.text = _(u'Remember Me')

    def validate_on_submit(self):
        rv = Form.validate(self)
        if not rv:
            return False
        m = hashlib.md5()
        m.update(self.password.data)
        m = m.hexdigest()
        user = User.query.filter_by(email=self.email.data, password=m[:-len(m)+250]).first()
        if user is None:
            self.email.errors.append(_(u'Email or Password is invalid.'))
            return False
        self.user = user
        return True


# /*-------------------------------------------------------------------------*/


def user_validate_rank(form, field):
    b = True
    for rank in app.config['RANKS']:
        if rank[0] == field.data:
            b = False
            if current_user.rank < rank[2]:
                raise ValidationError(_(u'You do not have enough rights.'))
    if b:
        raise ValidationError(_(u'No rank with id ') + field.data)

def user_validate_password(form, field):
    if not field.data == form.password.data:
        raise ValidationError(_(u'Passwords do not match.'))

class UserForm(Form):
    name = TextField(_(u'Name'), [
        validators.Length(min=2, max=250),
        validators.Required()
    ])
    email = TextField(_(u'Email'), [
        validators.Length(min=4, max=100),
        validators.Required()
    ])
    password = PasswordField(_(u'Password'), [
        validators.Length(max=250),
        validators.Required()
    ])
    password2 = PasswordField(_(u'Repeat Password'), [
        validators.Length(max=250),
        validators.Required(),
        user_validate_password
    ])
    lang = SelectField(_(u'Language'), choices=app.config['LANGUAGES'])
    rank = IntegerField(_(u'Rank'), [
        validators.NumberRange(min=1, max=10),
        validators.Required(),
        user_validate_rank
    ])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.name.label.text = _(u'Name')
        self.email.label.text = _(u'Email')
        self.password.label.text = _(u'Password')
        self.password2.label.text = _(u'Repeat Password')
        self.lang.label.text = _(u'Language')
        self.rank.label.text = _(u'Rank')

    def create_new(self):
        rv = Form.validate(self)
        if rv:
            u = User.query.filter_by(email=str(self.email.data).lower()).first()
            if not u is None:
                self.email.errors.appen(_(u'This email is already in use'))
                return False
            user = User()
            user.init(self.name.data, self.password.data, self.email.data, self.lang.data, self.rank.data, self.phone.data)
            db.session.add(user)
            db.session.commit()
            self.user = user
            return True
        return False

    def upgrade(self, user):
        r1 = self.name.validate(self)
        r2 = self.email.validate(self)
        r3 = self.lang.validate(self)
        r4 = self.rank.validate(self)
        if r1 and r2 and r3 and r4:
            u = User.query.filter_by(email=str(self.email.data).lower()).first()
            if (not u == user) and (not u is None):
                self.email.errors.appen(_(u'This email is already in use'))
                return False
            user.username = self.name.data
            user.set_email(self.email.data)
            user.lang = self.lang.data
            user.rank = self.rank.data
            user.set_phone(self.phone.data)
            db.session.add(user)
            db.session.commit()
            self.user = user
            return True
        return False

    def upgrade_password(self, user):
        r1 = self.password.validate(self)
        r2 = self.password2.validate(self)
        if r1 and r2:
            user.set_password(self.password.data)
            db.session.add(user)
            db.session.commit()
            self.user = user
            return True
        return False

class UploadForm(Form):
    img = FileField(_(u'Image'), validators=[
        FileRequired(),
        FileAllowed(app.config['IMAGES'], _(u'Images only'))
    ])

    def validate_img(self):
        return self.img.validate(self)

class UploadIconForm(Form):
    img = FileField(_(u'Icon'), validators=[
        FileRequired(),
        FileAllowed(app.config['ICONS'], _(u'PNG files only'))
    ])

    def validate_img(self):
        return self.img.validate(self)