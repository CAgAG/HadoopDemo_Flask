import os, shutil, datetime, uuid

from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify

from app.view import BASEURL
from app import HDFS
from app import database

UserApp = Blueprint('user', __name__)


@UserApp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@UserApp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@UserApp.route('/register_user', methods=['POST'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    if database.insert_user(username=username, password=password, email=email):
        return redirect(url_for('user.index'))
    else:
        return redirect(url_for('user.register'))


@UserApp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not database.check_user(username=username, password=password):
        return redirect(url_for('user.index'))
    else:
        return redirect(url_for('file_view.browser'))


@UserApp.route('/reset', methods=['GET'])
def reset_page():
    return render_template('reset.html')


@UserApp.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form.get('username')
    email = request.form.get('email')

    database.reset_user(username=username, email=email)
    return redirect(url_for('user.index'))


@UserApp.route('/workplace')
def workplace():
    ctx = {
        'url': BASEURL
    }
    return render_template('choices.html', **ctx)
