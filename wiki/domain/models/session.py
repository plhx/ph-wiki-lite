import datetime
import uuid
from .base import IValueObject, IEntity


__all__ = [
    'SessionId', 'SessionExpires', 'Session',
    'SessionError', 'SessionNotFoundError', 'SessionConflictError'
]


class SessionId(IValueObject):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError()
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))


class SessionExpires(IValueObject):
    def __init__(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError(value)
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError(value)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __lt__(self, other):
        if type(self) != type(other):
            raise TypeError(other)
        return self.value < other.value

    def __gt__(self, other):
        if type(self) != type(other):
            raise TypeError(other)
        return self.value > other.value


class Session(IEntity):
    def __init__(self, session_id: SessionId, expires: SessionExpires):
        if not isinstance(session_id, SessionId):
            raise TypeError(session_id)
        if not isinstance(expires, SessionExpires):
            raise TypeError(expires)
        self.session_id = session_id
        self.expires = expires

    @property
    def identity(self):
        return self.session_id.value


class SessionError(Exception):
    pass


class SessionNotFoundError(SessionError):
    pass


class SessionConflictError(SessionError):
    pass
