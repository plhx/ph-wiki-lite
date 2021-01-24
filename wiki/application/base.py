import abc


__all__ = [
    'IServiceRequest', 'IServiceResponse', 'IServiceHandler',
    'IDependencyResolver', 'ServiceMediator'
]


class IServiceRequest(metaclass=abc.ABCMeta):
    pass


class IServiceResponse(metaclass=abc.ABCMeta):
    pass


class IServiceHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, request: IServiceRequest) -> IServiceResponse:
        raise NotImplementedError()


class IDependencyResolver:
    @abc.abstractmethod
    def resolve(self, klass):
        raise NotImplementedError()


class ServiceMediator:
    def __init__(self, dependency: IDependencyResolver):
        self._dependency = dependency
        self._handlers = {}

    def bind(self, request_class, handler_class) -> None:
        self._handlers[request_class] = handler_class

    def call(self, request: IServiceRequest) -> IServiceResponse:
        if not isinstance(request, IServiceRequest):
            raise TypeError(request)
        handler = self._dependency.resolve(self._handlers[type(request)])
        response = handler.handle(request)
        if not isinstance(response, IServiceResponse):
            raise TypeError(response)
        return response
