import datetime
from .base import *
from ..dependencies import *
from ..domain.models.password import *
from ..domain.repositories.ipassword_repository import *


__all__ = [
    'PasswordGetAllRequest',
    'PasswordGetAllResponse',
    'PasswordGetAllHandler',
]


class PasswordGetAllRequest(IServiceRequest):
    pass


class PasswordGetAllResponse(IServiceResponse):
    def __init__(self, passwords: [HashedPassword]):
        self.passwords = passwords


class PasswordGetAllHandler(IServiceHandler):
    def __init__(self):
        self._password_repository = Dependency.resolve(IPasswordRepository)

    def handle(self, request: IServiceRequest):
        passwords = self._password_repository.getall()
        return PasswordGetAllResponse(passwords=passwords)
