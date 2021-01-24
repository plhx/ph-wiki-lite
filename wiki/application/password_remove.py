import datetime
from .base import *
from ..dependencies import *
from ..domain.models.password import *
from ..domain.repositories.ipassword_repository import *


__all__ = [
    'PasswordRemoveRequest',
    'PasswordRemoveResponse',
    'PasswordRemoveHandler',
]


class PasswordRemoveRequest(IServiceRequest):
    def __init__(self, password: HashedPassword):
        self.password = password


class PasswordRemoveResponse(IServiceResponse):
    pass


class PasswordRemoveHandler(IServiceHandler):
    def __init__(self):
        self._password_repository = Dependency.resolve(IPasswordRepository)

    def handle(self, request: IServiceRequest):
        self._password_repository.remove(request.password)
        return PasswordRemoveResponse()
