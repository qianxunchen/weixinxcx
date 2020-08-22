from flask import jsonify
import hashlib


def Success():
    data = {
        "msg":"操作成功",
        "status_code":"200"
    }
    return jsonify(data)

def Error():
    data = {
        "msg":"失败",
        "status_code":"404"
    }
    return jsonify(data)

md5 = hashlib.md5()

def md(password):
    md5.update(password.encode())
    pass_md =md5.hexdigest()
    return pass_md