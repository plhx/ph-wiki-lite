import datetime
from .base import *
from ..dependencies import *
from ..domain.models.password import *
from ..domain.models.session import *
from ..domain.repositories.ipassword_repository import *
from ..domain.repositories.isession_repository import *


__all__ = [
    'LoginError', 'LoginPasswordError',
    'LoginRequest', 'LoginResponse', 'LoginHandler',
]


class LoginError(Exception):
    pass


class LoginPasswordError(LoginError):
    pass


class LoginRequest(IServiceRequest):
    def __init__(self, password: Password):
        self.password = password


class LoginResponse(IServiceResponse):
    def __init__(self, session: Session):
        self.session = session


class LoginHandler(IServiceHandler):
    def __init__(self):
        self._password_repository = Dependency.resolve(IPasswordRepository)
        self._session_repository = Dependency.resolve(ISessionRepository)

    def handle(self, request: IServiceRequest):
        for password in self._password_repository.getall():
            hashed = HashedPassword.frompassword(
                request.password,
                password.secret
            )
            if hashed == password:
                break
        else:
            raise LoginPasswordError()
        session = Session(
            session_id=SessionId.generate(),
            expires=SessionExpires(datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=30))
        )
        self._session_repository.save(session)
        self._session_repository.purge()
        return LoginResponse(session)
