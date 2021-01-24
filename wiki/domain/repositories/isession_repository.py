import abc
from ..models.session import SessionId, Session


__all__ = ['ISessionRepository']


class ISessionRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, session_id: SessionId) -> Session:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, session: Session) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, session: Session) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def purge(self) -> None:
        raise NotImplementedError()
