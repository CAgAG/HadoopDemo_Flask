SUCCESS = 400
FAIL = 500


def success_message(data, message='发送成功'):
    ctx = {
        'code': SUCCESS,
        'msg': message,
        'data': data
    }
    return ctx


def fail_message(data, message='发送失败'):
    ctx = {
        'code': FAIL,
        'msg': message,
        'data': data
    }
    return ctx
