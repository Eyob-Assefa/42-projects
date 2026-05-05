from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name: str = name
        self.creature_type: str = creature_type

    @abstractmethod
    def attack(self) -> str:
        """
        This is an abstract method. 
        It has no code inside it (just 'pass').
        Any class that inherits from Creature MUST write its own attack method.
        """
        pass

    def describe(self) -> str:
        """
        This is a concrete method. 
        All creatures will use this exact same code to describe themselves.
        """
        return f"{self.name} is a {self.creature_type} type Creature"

# Assuming the Creature class is above this in the same file...

class Flameling(Creature):
    def __init__(self) -> None:
        # We pass the specific name and type up to the parent Creature blueprint
        super().__init__(name="Flameling", creature_type="Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__(name="Pyrodon", creature_type="Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    def __init__(self) -> None:
        super().__init__(name="Aquabub", creature_type="Water")

    def attack(self) -> str:
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    def __init__(self) -> None:
        super().__init__(name="Torragon", creature_type="Water")

    def attack(self) -> str:
        return f"{self.name} uses Hydro Pump!"

