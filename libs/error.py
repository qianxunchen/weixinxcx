from flask import request, json
from werkzeug.exceptions import HTTPException
#自定义基类异常
class APIException(HTTPException):
    code = 500
    msg = '未知错误'
    error_code = 999
    #'headers':html头数据
    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)
    #返回一个josn类型的异常
    def get_body(self, environ=None):
        body = dict(
            msg = self.msg,
            error_code = self.error_code,
            request = request.method + '' + self.get_url_no_param()
        )
        #json序列化
        text = json.dumps(body)
        return text
    #更改头数据
    def get_headers(self, environ=None):
        return [('Context-Type', 'application/json')]
    @classmethod
    def get_url_no_param(cls):
        #得到请求的url
        full_path = str(request.full_path)
        #去除'?'后面的数据
        main_path = full_path.split('?')
        return main_path[0]