import sqlite3
import injector
from ..database.idatabase import IDatabase
from ...domain.models.password import HashedPassword, PasswordSecret
from ...domain.repositories.ipassword_repository import IPasswordRepository


__all__ = ['PasswordRepository']


class PasswordRepository(IPasswordRepository):
    @injector.inject
    def __init__(self, database: IDatabase):
        self.database = database
        cur = self.database.context.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS [password] (
            [hash] TEXT NOT NULL,
            [secret] BLOB NOT NULL
        )''')
        self.database.context.commit()

    def getall(self) -> [HashedPassword]:
        cur = self.database.context.cursor()
        cur.execute('SELECT [hash], [secret] FROM [password]')
        return [HashedPassword(value=hash, secret=PasswordSecret(secret))
            for hash, secret in cur.fetchall()]

    def save(self, password: HashedPassword) -> None:
        cur = self.database.context.cursor()
        cur.execute('''REPLACE INTO [password]
            ([hash], [secret]) VALUES (:hash, :secret)''',
            {'hash': password.value, 'secret': password.secret.value}
        )
        self.database.context.commit()

    def remove(self, password: HashedPassword) -> None:
        cur = self.database.context.cursor()
        cur.execute('''DELETE FROM [password] WHERE
            [hash] = :hash AND [secret] = :secret''',
            {'hash': password.value, 'secret': password.secret.value}
        )
        self.database.context.commit()

    def removeall(self) -> None:
        cur = self.database.context.cursor()
        cur.execute('DELETE FROM [password]')
        self.database.context.commit()
