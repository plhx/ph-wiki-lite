import datetime
from .base import *
from ..dependencies import *
from ..domain.models.password import *
from ..domain.repositories.ipassword_repository import *


__all__ = [
    'PasswordAddRequest',
    'PasswordAddResponse',
    'PasswordAddHandler',
]


class PasswordAddRequest(IServiceRequest):
    def __init__(self, password: Password):
        self.password = password


class PasswordAddResponse(IServiceResponse):
    pass


class PasswordAddHandler(IServiceHandler):
    def __init__(self):
        self._password_repository = Dependency.resolve(IPasswordRepository)

    def handle(self, request: IServiceRequest):
        secret = PasswordSecret.generate()
        hashed = HashedPassword.frompassword(request.password, secret)
        self._password_repository.save(hashed)
        return PasswordAddResponse()
