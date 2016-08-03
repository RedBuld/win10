from flask import Blueprint, render_template, redirect, abort, g, session, request, flash, url_for, session, Flask
from flask_login import login_user, logout_user, current_user, login_required
from flask_babelex import lazy_gettext, gettext as _, ngettext
from .. import app, db, babel
from ..models import User
from ..forms import UserForm
from ..tools import check_rank_user, check_rank


user_module = Blueprint('user_module', __name__)

@user_module.route('/change_language')
@user_module.route('/change_language/<string:lang>')
@login_required
def change_language(lang=''):
    if not lang == '':
        for i in app.config['LANGUAGES']:
            if i[0] == lang:
                current_user.locale = lang
                db.session.add(current_user)
                db.session.commit()
                return redirect(request.args.get('next') or url_for('index'))
        return abort(404)
    return render_template('user/change_language.html', next=(request.args.get('next') or url_for('index')))

@user_module.route('/list')
@user_module.route('/list/<int:page>')
@login_required
def list(page=1):
    if not check_rank(3):
        return abort(403)
    per_page = 30
    query = ''
    if not request.args.get('q') is None:
        query = request.args.get('q') 
        users = User.query.filter(User.rank<5, User.username.ilike('%'+query+'%'), User.rank<current_user.rank).paginate(page, per_page, False)
    else:
        users = User.query.filter(User.rank<5, User.rank<current_user.rank).paginate(page, per_page, False)
    return render_template('user/list.html', users=users, query=query)

@user_module.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not check_rank(3):
        return abort(403)
    form = UserForm(request.form)
    if request.method == 'POST':
        rv = form.create_new()
        if rv:
            flash(_('User successfully created'), 'success')
            return redirect(url_for('user_module.edit', user_id=form.user.id))
    return render_template('user/new.html', form=form)

@user_module.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        return abort(404)
    if not check_rank_user(user.rank):
        return abort(403)
    form = UserForm(request.form)
    if request.method == 'POST':
        if str(request.args.get('password')) == '1':
            form.upgrade_password(user)
        else:
            form.upgrade(user)
    return render_template('user/edit.html', form=form, user=user)

@user_module.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        return abort(404)
    if not check_rank_user(user.rank):
        return abort(403)
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash(_('User successfully deleted'), 'success')
        return redirect(url_for('user_module.list'))
    return render_template('user/delete.html', user=user)
