from app import ES, db, models


def db_commit():
    try:
        db.session.commit()
    except Exception as e:
        return False
    return True


def insert_user(username: str, password: str, email: str):
    user = models.User()
    user.username = username
    user.password = password
    user.email = email
    db.session.add(user)
    return db_commit()


def check_user(username: str, password: str):
    user = models.User()

    users = user.query.filter_by(username=username).all()
    if len(users) == 0:
        return False
    fuser = users[0]
    if fuser.password == password:
        return True
    return False


def reset_user(username: str, email: str):
    user = models.User()

    users = user.query.filter_by(username=username, email=email).all()
    if len(users) != 0:
        users[0].password = '123456'
        db_commit()


def insert_file(filename: str, filepath: str, content: str):
    data = {
        'filename': filename,
        'filepath': filepath,
        'content': content
    }
    try:
        ES.insert2(data=data)
    except Exception:
        return False
    return True


def query_file(data: dict):
    id_list, data_list = ES.query2(data=data)
    return id_list, data_list


def delete_file(data: dict):
    ES.delete2(data=data)
