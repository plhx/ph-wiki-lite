import sqlite3
import injector
from .idatabase import IDatabase


class SQLite3Database(IDatabase):
    def __init__(self, path):
        self.path = path
        self._context = sqlite3.connect(
            path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )

    def close(self):
        self._context.close()

    @property
    def context(self):
        return self._context
