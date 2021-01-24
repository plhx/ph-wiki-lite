import datetime
import sqlite3
import injector
from ..database.idatabase import IDatabase
from ...domain.models.session import *
from ...domain.repositories.isession_repository import ISessionRepository


__all__ = ['SessionRepository']


class SessionRepository(ISessionRepository):
    @injector.inject
    def __init__(self, database: IDatabase):
        self.database = database
        cur = self.database.context.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS [session] (
            [session_id] TEXT PRIMARY KEY,
            [expires] TIMESTAMP NOT NULL
        )''')
        self.database.context.commit()

    def get(self, session_id: SessionId) -> Session:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [session_id], [expires] FROM [session]
            WHERE [session_id] = :session_id''',
            {'session_id': session_id.value}
        )
        row = cur.fetchone()
        if row is None:
            raise SessionNotFoundError()
        session_id, expires = row
        return Session(
            session_id=SessionId(session_id),
            expires=SessionExpires(expires.astimezone(datetime.timezone.utc))
        )

    def save(self, session: Session) -> None:
        cur = self.database.context.cursor()
        cur.execute('''REPLACE INTO [session]
            ([session_id], [expires]) VALUES (:session_id, :expires)''',
            {k: v.value for k, v in session.__dict__.items()}
        )
        self.database.context.commit()

    def remove(self, session: Session) -> None:
        cur = self.database.context.cursor()
        cur.execute(
            'DELETE FROM [session] WHERE [session_id] = :session_id',
            {k: v.value for k, v in session.__dict__.items()}
        )
        self.database.context.commit()

    def purge(self) -> None:
        cur = self.database.context.cursor()
        cur.execute(
            'DELETE FROM [session] WHERE [expires] < :now',
            {'now': datetime.datetime.utcnow()}
        )
        self.database.context.commit()
