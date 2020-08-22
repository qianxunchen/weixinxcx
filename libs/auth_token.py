from flask import g, current_app, jsonify
from collections import namedtuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_httpauth import HTTPBasicAuth
from libs.error_code import AuthFailed


auth = HTTPBasicAuth()
User = namedtuple('User', ['id'])

@auth.verify_password# 使verify_password()作为@auth.login_requeried回调函数使用
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # 将令牌信息保存到g.user里面，使其他也可以使用
        g.user = user_info
        return True

# 验证令牌
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # 解密令牌，获取信息
        data = s.loads(token)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1002)  # 令牌存在，过期了
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1003)  # 令牌不存在
    id = data['id']
    return User(id)

# 生成令牌，参数意义：scope：权限设置；expiration：过期时间(单位：秒)
def generate_token(api_users, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration) #expiration是过期时间
    token = s.dumps({
        'id': api_users
        })
    return token

