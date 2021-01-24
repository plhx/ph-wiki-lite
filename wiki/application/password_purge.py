import datetime
from .base import *
from ..dependencies import *
from ..domain.models.password import *
from ..domain.repositories.ipassword_repository import *


__all__ = [
    'PasswordPurgeRequest',
    'PasswordPurgeResponse',
    'PasswordPurgeHandler',
]


class PasswordPurgeRequest(IServiceRequest):
    pass


class PasswordPurgeResponse(IServiceResponse):
    pass


class PasswordPurgeHandler(IServiceHandler):
    def __init__(self):
        self._password_repository = Dependency.resolve(IPasswordRepository)

    def handle(self, request: IServiceRequest):
        self._password_repository.removeall()
        return PasswordPurgeResponse()
