import datetime
import sqlite3
import injector
from ..database.idatabase import IDatabase
from ...domain.models.page import *
from ...domain.repositories.ipage_repository import IPageRepository


__all__ = ['PageRepository']


class PageRepository(IPageRepository):
    @injector.inject
    def __init__(self, database: IDatabase):
        self.database = database
        cur = self.database.context.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS [page] (
            [page_id] TEXT PRIMARY KEY,
            [title] TEXT NOT NULL,
            [body] TEXT NOT NULL,
            [lastmodified] TIMESTAMP NOT NULL,
            [version] INTEGER NOT NULL
        )''')
        self.database.context.commit()

    def get(self, page_id: PageId) -> Page:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [page_id], [title], [body],
            [lastmodified], [version] FROM [page]
            WHERE [page_id] = :page_id''',
            {'page_id': page_id.value}
        )
        row = cur.fetchone()
        if row is None:
            raise PageNotFoundError(page_id)
        page_id, title, body, lastmodified, version = row
        return Page(
            page_id=PageId(page_id),
            title=PageTitle(title),
            body=PageBody(body),
            lastmodified=PageLastModified(
                lastmodified.astimezone(datetime.timezone.utc)
            ),
            version=PageVersion(version)
        )

    def getall(self) -> [Page]:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [page_id], [title], [body],
            [lastmodified], [version] FROM [page]''',
        )
        return [Page(
            page_id=PageId(page_id),
            title=PageTitle(title),
            body=PageBody(body),
            lastmodified=PageLastModified(
                lastmodified.astimezone(datetime.timezone.utc)
            ),
            version=PageVersion(version)
        ) for page_id, title, body, lastmodified, version in cur.fetchall()]

    def save(self, page: Page) -> None:
        cur = self.database.context.cursor()
        try:
            self.get(page.page_id)
            cur.execute('''UPDATE [page] SET [title] = :title, [body] = :body,
                [lastmodified] = :lastmodified, [version] = :version + 1
                WHERE [page_id] = :page_id AND [version] = :version''',
                {k: v.value for k, v in page.__dict__.items()}
            )
        except PageNotFoundError:
            cur.execute('''INSERT INTO [page]
                ([page_id], [title], [body], [lastmodified], [version])
                VALUES (:page_id, :title, :body, :lastmodified, 0)''',
                {k: v.value for k, v in page.__dict__.items()}
            )
        if cur.rowcount != 1:
            raise PageVersionConflictError()
        self.database.context.commit()

    def remove(self, page: Page) -> None:
        cur = self.database.context.cursor()
        cur.execute(
            'DELETE FROM [page] WHERE [page_id] = :page_id',
            {k: v.value for k, v in page.__dict__.items()}
        )
        self.database.context.commit()
