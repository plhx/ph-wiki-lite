import hashlib
import hmac
import secrets
from .base import IValueObject, IEntity


class Password(IValueObject):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


class PasswordSecret(IValueObject):
    def __init__(self, value):
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(value)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    @classmethod
    def generate(cls, length=32):
        return cls(secrets.token_bytes(length))


class HashedPassword(IValueObject):
    def __init__(self, value, secret):
        if not isinstance(value, str):
            raise TypeError(value)
        if not isinstance(secret, PasswordSecret):
            raise TypeError(secret)
        self.value = value
        self.secret = secret

    def __eq__(self, other):
        return type(self) == type(other) \
            and self.value == other.value \
            and self.secret == other.secret

    @classmethod
    def frompassword(cls, password, secret):
        hashed = hmac.HMAC(
            secret.value,
            password.value.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return cls(hashed, secret)
