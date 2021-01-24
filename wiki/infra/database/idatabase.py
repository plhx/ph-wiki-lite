import abc


__all__ = ['IDatabase']


class IDatabase(metaclass=abc.ABCMeta):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def context(self):
        raise NotImplementedError()
