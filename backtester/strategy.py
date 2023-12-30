from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def long():
        pass

    @abstractmethod
    def short():
        pass

    @abstractmethod
    def close():
        pass
