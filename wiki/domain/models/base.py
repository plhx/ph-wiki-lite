import abc


class IValueObject(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __eq__(self, other):
        raise NotImplementedError()


class IEntity(metaclass=abc.ABCMeta):
    def __eq__(self, other):
        raise self.identity == other.identity

    @property
    @abc.abstractmethod
    def identity(self):
        raise NotImplementedError()
