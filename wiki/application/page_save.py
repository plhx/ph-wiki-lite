from .base import *
from ..dependencies import *
from ..domain.models.page import *
from ..domain.repositories.ipage_repository import *


__all__ = ['PageSaveRequest', 'PageSaveResponse', 'PageSaveHandler']


class PageSaveRequest(IServiceRequest):
    def __init__(self, page: Page):
        self.page = page


class PageSaveResponse(IServiceResponse):
    pass


class PageSaveHandler(IServiceHandler):
    def __init__(self):
        self._page_repository = Dependency.resolve(IPageRepository)

    def handle(self, request: IServiceRequest):
        if request.page.body.value:
            page = self._page_repository.save(request.page)
        else:
            self._page_repository.remove(request.page)
        return PageSaveResponse()
