import os, shutil, datetime, uuid

from flask import Blueprint, render_template, \
    request, redirect, url_for, session, jsonify, send_file

from app.view import BASEURL, ResultCode
from app import HDFS, database

FileViewApp = Blueprint('file_view', __name__)


def read_file_content(path: str):
    with open(path, 'r', encoding='UTF-8') as f:
        return f.read()


@FileViewApp.route('/upload', methods=['GET'])
def upload_Page():
    path = session.get('cur_path', '/')
    ctx = {
        'cur_path': path,
        'base_url': BASEURL
    }
    return render_template('upload_files.html', **ctx)


@FileViewApp.route('/upFile', methods=['POST'])
def upFile_Post():
    cur_path = session.get('cur_path', '/')

    file = request.files.get('file')
    filename = f"{file.filename}"

    basepath = f"{datetime.datetime.now().strftime('%Y-%m-%d-%H')}/"
    fullpath = f'app/media/{basepath}'
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
        fullpath = os.path.join(fullpath, filename)
    else:
        tfullpath = os.path.join(fullpath, filename)
        i = 0
        while os.path.exists(tfullpath):
            i += 1
            filename2 = f'({i}){filename}'
            tfullpath = os.path.join(fullpath, filename2)
        fullpath = tfullpath

    basepath = os.path.join(basepath, filename)
    file.save(fullpath)
    # 记录 ES
    file_content = read_file_content(fullpath)
    database.insert_file(filename=filename, content=file_content, filepath=cur_path)

    if os.path.exists(fullpath):
        ab_path = os.path.abspath(fullpath)
        HDFS.upload_file(pdir=f'{cur_path}/{filename}'.replace('//', '/'), local_path=ab_path)
        jsdata = {
            "code": ResultCode.SUCCESS,
            "msg": "上传成功",  # 提示信息 一般上传失败后返回
            "data": {
                "src": '../../show/' + basepath,
                "title": filename  # 可选
            }
        }

        return jsonify(jsdata)
    else:
        jsdata = {
            "code": ResultCode.FAIL,
            "msg": "上传失败",  # 提示信息 一般上传失败后返回
            "data": {
                "src": '../../show/' + basepath,
                "title": filename  # 可选
            }
        }

        return jsonify(jsdata)


@FileViewApp.route('/browser', methods=['GET', 'POST'])
def browser():
    path = request.values.get('path', '')
    if path == '':
        path = HDFS.path_exist(session.get('cur_path', '/'))
    session['cur_path'] = path

    print(path)
    rets = []
    p_list = HDFS.list_path(path)
    for l in p_list:
        length = HDFS.file_property_length(os.path.join(path, l).replace('\\', '/'))
        ret = {
            'name': l,
            'length': length
        }
        # dir
        if length == 0:
            ret['type'] = 0
        else:
            ret['type'] = 1
        rets.append(ret)

    ctx = {
        'rets': rets,
        'url': f'{BASEURL}/file_view/get_file',
        'url2': f'{BASEURL}/file_view/delete_file',
        'url3': f'{BASEURL}/file_view/download_file',
        'path': path
    }

    return render_template('show_files.html', **ctx)


@FileViewApp.route('/get_file', methods=['GET', 'POST'])
def get_file():
    path = request.values.get('path', '/')
    if path == '../':
        path = session.get('cur_path', '/')
        path = os.path.dirname(path)
    else:
        path = session.get('cur_path', '/') + '/' + path
    path = path.replace('//', '/')
    session['cur_path'] = path

    return redirect(url_for('file_view.browser'))


@FileViewApp.route('/create_dir', methods=['POST'])
def create_dir():
    path = session.get('cur_path', '/')
    dirname = request.form.get('dirname')
    HDFS.create_dir(pdir=path, dirname=dirname)

    return redirect(url_for('file_view.browser'))


@FileViewApp.route('/delete_file', methods=['POST'])
def delete_file():
    path = session.get('cur_path', '/')
    filename = request.form.get('path')
    HDFS.delete_file(pdir=path, filename=filename)
    body = {
        'filepath': f'{path}/{filename}'.replace('//', '/')
    }
    database.delete_file(data=body)

    return redirect(url_for('file_view.browser'))


@FileViewApp.route('/download_file', methods=['POST'])
def download_file():
    path = session.get('cur_path', '/')
    filename = request.form.get('path')
    local_path = f'app/media/{path}/'
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    local_path = f'{local_path}/{filename}'
    HDFS.download_file(h_path=f'{path}/{filename}'.replace('//', '/'),
                       local_path=local_path)
    if os.path.exists(local_path):
        return jsonify({
            'f_url': f'/show/{path}/{filename}'.replace('//', '/'),
            'filename': filename
        })
    else:
        return redirect(url_for('file_view.browser'))


@FileViewApp.route('/clear', methods=['GET'])
def clear():
    session['cur_path'] = '/'
    return redirect(url_for('file_view.browser'))


@FileViewApp.route('/reset_path', methods=['GET'])
def reset_path():
    r_path = request.args.get('r_path', '/')
    session['cur_path'] = r_path
    return redirect(url_for('file_view.browser'))
