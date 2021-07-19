from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify

from app.view import BASEURL
from app import database

SearchApp = Blueprint('search', __name__)


@SearchApp.route('/sub_search', methods=['GET'])
def sub_search():
    ctx = {
        'url': BASEURL
    }
    return render_template('search.html', **ctx)


@SearchApp.route('/search_result', methods=['GET', 'POST'])
def search_result():
    email = request.form.get('email', '')
    username = request.form.get('username', '')
    data = {}
    if email != '':
        data['email'] = email
    if username != '':
        data['username'] = username

    id_list, user_list = database.query_id_user(data=data)

    ctx = {
        'url': f'{BASEURL}/search/delete_user',
        'url2': f'{BASEURL}/search/update_user',
        'user_list': user_list,
        'id_list': id_list
    }
    return render_template('search_result.html', **ctx)


@SearchApp.route('/delete_user', methods=['POST'])
def delete_user():
    username = request.form.get('username', '')
    if id != '':
        database.delete_user(username=username)

    return redirect(url_for('search.sub_search'))


@SearchApp.route('/update_user', methods=['POST'])
def update_user():
    id = request.form.get('id', '')
    data = {}

    database.update_user(data=data, cid=id)
    return redirect(url_for('search.sub_search'))


@SearchApp.route('/search_file', methods=['POST'])
def search_file():
    # 获得输入的关键词
    key_file = request.form.get('key_file', '')
    # 构造检索参数
    data = {
        'content': key_file
    }
    # 得到处理后检索结果
    _, data_list = database.query_file(data=data)
    ctx = {
        'data_list': data_list
    }
    # 返回检索结果页面
    return render_template('search_file_result.html', **ctx)
