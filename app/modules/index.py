# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, abort, g, session, request, flash, url_for, Flask
from flask_login import login_user, logout_user, current_user, login_required
from flask_babelex import lazy_gettext, gettext as _, ngettext
from .. import app, db, babel
from ..models import User
from ..forms import UserForm
from ..tools import check_rank_user, check_rank

index_module = Blueprint('index_module', __name__)

@index_module.route('/')
def index():
	return render_template('index/index.html')