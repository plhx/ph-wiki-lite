import abc
from ..models.password import HashedPassword
from ..models.session import SessionId, Session


__all__ = ['IPasswordRepository']


class IPasswordRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getall(self) -> [HashedPassword]:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, password: HashedPassword) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, password: HashedPassword) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def removeall(self) -> None:
        raise NotImplementedError()
