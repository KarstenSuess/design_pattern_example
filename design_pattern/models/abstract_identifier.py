from abc import ABC, abstractmethod

class AbstractIdentifier(ABC):
    @abstractmethod
    def identify(self, fileName: str):
        pass
