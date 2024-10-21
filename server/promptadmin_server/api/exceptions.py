from typing import Any

from fastapi import HTTPException


class ApiException(HTTPException):
    STATUS_CODE = 500
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionException(ApiException):
    STATUS_CODE = 403
    DETAIL = "Permission denied"


class ProjectConnectionException(ApiException):
    STATUS_CODE = 501
    DETAIL = "Cant connect to the project"


class TypeCheckException(ApiException):
    STATUS_CODE = 502
    DETAIL = "Received an object that was not expected"


class SQLDBException(ApiException):
    STATUS_CODE = 503
    DETAIL = "SQL request throw exception"
