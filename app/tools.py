import os, os.path, pytz
import hashlib, string, random
from werkzeug import secure_filename
from flask import Blueprint, render_template, redirect, abort, g, session, request, flash, url_for, Flask
from flask_login import login_user, logout_user, current_user, login_required
from flask_babelex import lazy_gettext, gettext as _, ngettext
from app import app, babel
from datetime import datetime


def check_rank_user(rank):
    for i in app.config['RANKS']:
        if i[0] == rank:
            if current_user.rank >= i[2]:
                return True
    return False

def check_rank(rank):
    if current_user.rank >= rank:
        return True
    return False

def get_filename(directory, f):
    filenames = os.listdir(directory)
    b = True
    try:
        ext = f[f.rfind('.'):]
    except Exception, e:
        ext = ''
    while b:
        t = True
        s = string.digits + string.ascii_letters
        f = secure_filename(''.join(random.choice(s) for x in range(30))+ext)
        print f
        for filename in filenames:
            if filename == f:
                t = False
        if t:
            b = False
    return f

def remove_img(url):
    os.remove(app.config['UPLOADS_FOLDER'] + '/' + url)
    filenames = os.listdir(app.config['MEDIA_THUMBNAIL_FOLDER'])
    for filename in filenames:
        name = url[:url.rfind('.')]
        name2 = filename[:filename.index('_')]
        if name == name2:
            os.remove(app.config['MEDIA_THUMBNAIL_FOLDER'] + '/' + filename)


def remove_icon(url):
    os.remove(app.config['UPLOADS_ICON_FOLDER'] + '/' + url)


def check_img(url):
    return os.path.isfile(app.config['UPLOADS_FOLDER'] + '/' + url)


def check_icon(url):
    return os.path.isfile(app.config['UPLOADS_ICON_FOLDER'] + '/' + url)