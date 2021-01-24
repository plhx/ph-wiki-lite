import abc
from ..models.page import PageId, Page


__all__ = ['IPageRepository']


class IPageRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, page_id: PageId) -> Page:
        raise NotImplementedError()

    @abc.abstractmethod
    def getall(self) -> [Page]:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, page: Page) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, page: Page) -> None:
        raise NotImplementedError()
