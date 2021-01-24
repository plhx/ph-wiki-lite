from .base import *
from ..dependencies import *
from ..domain.models.session import *
from ..domain.repositories.isession_repository import *


__all__ = ['LogoutRequest', 'LogoutResponse', 'LogoutHandler']


class LogoutRequest(IServiceRequest):
    def __init__(self, session: Session):
        self.session = session


class LogoutResponse(IServiceResponse):
    def __init__(self):
        pass


class LogoutHandler(IServiceHandler):
    def __init__(self):
        self._session_repository = Dependency.resolve(ISessionRepository)

    def handle(self, request: IServiceRequest):
        self._session_repository.remove(request.session)
        return LogoutResponse()
