from .dependencies import Dependency
from .application.base import ServiceMediator
from .application.login import *
from .application.logout import *
from .application.page_get import *
from .application.page_save import *
from .application.password_getall import *
from .application.password_add import *
from .application.password_remove import *
from .application.password_purge import *


__all__ = ['Service']


Service = ServiceMediator(Dependency)

Service.bind(LoginRequest, LoginHandler)
Service.bind(LogoutRequest, LogoutHandler)
Service.bind(PageGetRequest, PageGetHandler)
Service.bind(PageSaveRequest, PageSaveHandler)
Service.bind(PasswordGetAllRequest, PasswordGetAllHandler)
Service.bind(PasswordAddRequest, PasswordAddHandler)
Service.bind(PasswordRemoveRequest, PasswordRemoveHandler)
Service.bind(PasswordPurgeRequest, PasswordPurgeHandler)
