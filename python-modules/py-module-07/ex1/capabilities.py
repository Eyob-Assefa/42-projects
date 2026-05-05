from abc import ABC, abstractmethod

class HealCapability(ABC):
    """Abstract capability for healing actions."""
    
    @abstractmethod
    def heal(self) -> str:
        pass


class TransformCapability(ABC):
    """Abstract capability for transforming actions."""
    
    def __init__(self) -> None:
        # This is the persistent state attribute required by the instructions.
        # It allows the creature to remember if it is currently transformed.
        self.is_transformed = False 
        
    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass