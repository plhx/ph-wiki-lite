import datetime
from .base import IValueObject, IEntity


__all__ = [
    'PageId', 'PageTitle', 'PageBody', 'PageLastModified', 'PageVersion',
    'Page',
    'PageError', 'PageNotFoundError', 'PageVersionConflictError'
]


class PageId(IValueObject):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


class PageTitle(IValueObject):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


class PageBody(IValueObject):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


class PageLastModified(IValueObject):
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

    @classmethod
    def now(cls):
        return cls(datetime.datetime.now(datetime.timezone.utc))


class PageVersion(IValueObject):
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError()
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


class Page(IEntity):
    def __init__(self, page_id: PageId, title: PageTitle, body: PageBody,
        lastmodified: PageLastModified, version: PageVersion):
        if not isinstance(page_id, PageId):
            raise TypeError(page_id)
        if not isinstance(title, PageTitle):
            raise TypeError(title)
        if not isinstance(body, PageBody):
            raise TypeError(body)
        if not isinstance(lastmodified, PageLastModified):
            raise TypeError(lastmodified)
        if not isinstance(version, PageVersion):
            raise TypeError(version)
        self.page_id = page_id
        self.title = title
        self.body = body
        self.lastmodified = lastmodified
        self.version = version

    @property
    def identity(self):
        return self.page_id.value


class PageError(Exception):
    pass


class PageNotFoundError(PageError):
    pass


class PageVersionConflictError(PageError):
    pass
