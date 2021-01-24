import datetime
from .base import *
from ..dependencies import *
from ..domain.models.page import *
from ..domain.repositories.ipage_repository import *


__all__ = ['PageGetRequest', 'PageGetResponse', 'PageGetHandler']


class PageGetRequest(IServiceRequest):
    def __init__(self, page_id: PageId):
        self.page_id = page_id


class PageGetResponse(IServiceResponse):
    def __init__(self, page: Page):
        self.page = page


class PageGetHandler(IServiceHandler):
    def __init__(self):
        self._page_repository = Dependency.resolve(IPageRepository)

    def handle(self, request: IServiceRequest):
        try:
            page = self._page_repository.get(request.page_id)
        except PageNotFoundError:
            page = Page(
                page_id=request.page_id,
                title=PageTitle(''),
                body=PageBody(''),
                lastmodified=PageLastModified(
                    datetime.datetime.now(datetime.timezone.utc)
                ),
                version=PageVersion(0)
            )
        return PageGetResponse(page=page)
