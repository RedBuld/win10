from time import time
from flask import make_response, send_from_directory, Blueprint, render_template, redirect, abort, g, session, request, flash, url_for, Flask
from flask_login import login_user, logout_user, current_user, login_required
from flask_babelex import lazy_gettext, gettext as _, ngettext
from app import app, babel, thumb
from app.models import User
from app.forms import LoginForm, UserForm
from app.modules.user import user_module
from app.modules.index import index_module


# @app.route('/media/<regex("([\w\d_/-]+)?.(?:jpe?g|gif|png)"):filename>')
@app.route('/media/<path:filename>')
def media_file(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@babel.localeselector
def get_locale():
    if current_user.is_authenticated():
        # print current_user.locale
        return current_user.locale
    return request.accept_languages.best_match(['en', 'ru'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        logout_user()
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user, remember = form.remember_me)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
    return redirect(url_for('login'))


# /*-------------------------------------------------------------------------*/


@app.route('/admin')
@login_required
def index():
    if current_user.rank == 1:
        return redirect(url_for('driver_module.orders'))
    return redirect(url_for('order_module.list'))


@app.route('/admin/toggle_help')
@login_required
def toggle_help():
    response = make_response(redirect(request.args.get('next') or url_for('index')))
    if request.cookies.get('help-cont') is None or request.cookies.get('help-cont') == '':
        response.set_cookie('help-cont', 'remove', time() + (2 * 365 * 24 * 60 * 60))
    else:
        response.set_cookie('help-cont', '', time() + (2 * 365 * 24 * 60 * 60))
    return response

app.register_blueprint(user_module, url_prefix='/admin/user')
app.register_blueprint(index_module, url_prefix='')
