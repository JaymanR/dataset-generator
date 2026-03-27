from abc import ABC, abstractmethod
from config import GenerationConfig

class BaseGenerator(ABC):
    """Interface for generators"""
    
    def __init__(self, gen_config: GenerationConfig):
        self.gen_config = gen_config
        
    @abstractmethod
    def generate(self, prompt: str, n: int) -> list[str]:
        """"""
        ...
        
    @abstractmethod
    def is_available(self) -> bool:
        ...
        
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} config={self.gen_config}>"