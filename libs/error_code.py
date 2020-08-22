from libs.error import APIException
class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0
class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000
class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed '
    error_code = 1005
class NumberFailed(APIException):
    code = 402
    msg = 'Lack of stock'
    error_code = 4002
class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'
class NotFound(APIException):
    code = 404
    msg = 'the resource are not found '
    error_code = 1001
class RegisteredError(APIException):
    code = 406
    msg = 'the account have error'
    error_code = 1006
class ServeError(APIException):
    code = 500
    msg = 'sorry we made a mistake'
    error_code = 999




