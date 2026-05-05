from abc import ABC, abstractmethod
from ex0.creatures import Creature
from ex1.capabilities import HealCapability, TransformCapability

# 1. Define our custom exception
class InvalidStrategyError(Exception):
    """Raised when a strategy is applied to an incompatible creature."""
    pass

# 2. Define the Abstract Strategy
class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> None:
        pass

# 3. Define the Concrete Strategies
class NormalStrategy(BattleStrategy):
    """Suitable for any creature. Just attacks."""
    def is_valid(self, creature: Creature) -> bool:
        # Any creature can use the normal strategy
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(f"Invalid Creature '{creature.name}' for normal strategy")
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    """Suitable for transforming creatures. Transforms, attacks, reverts."""
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(f"Invalid Creature '{creature.name}' for this aggressive strategy")
        
        # We tell the type checker we know it has these methods
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    """Suitable for healing creatures. Attacks, then heals."""
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(f"Invalid Creature '{creature.name}' for this defensive strategy")
        
        print(creature.attack())
        print(creature.heal())