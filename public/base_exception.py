# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException
from rest_framework import status

class APIValidateException(APIException):
    def __init__(self, detail=u"未定义", status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code