import injector
from .application.base import IDependencyResolver
from .domain.repositories.ipage_repository import IPageRepository
from .domain.repositories.ipassword_repository import IPasswordRepository
from .domain.repositories.isession_repository import ISessionRepository
from .infra.database.idatabase import IDatabase
from .infra.database.sqlite3_database import SQLite3Database
from .infra.repositories.page_repository import PageRepository
from .infra.repositories.password_repository import PasswordRepository
from .infra.repositories.session_repository import SessionRepository


__all__ = ['Dependency']


class DependencyConfigure(IDependencyResolver):
    def __init__(self):
        self.injector = injector.Injector(self.__class__.configure)

    @classmethod
    def configure(self, binder):
        binder.bind(IDatabase, to=lambda: SQLite3Database('wiki.db'))
        binder.bind(IPageRepository, PageRepository)
        binder.bind(IPasswordRepository, PasswordRepository)
        binder.bind(ISessionRepository, SessionRepository)

    def resolve(self, klass):
        return self.injector.get(klass)


Dependency = DependencyConfigure()
