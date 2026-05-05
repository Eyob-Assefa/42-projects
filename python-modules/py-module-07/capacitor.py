from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1 import HealCapability, TransformCapability


def test_healing_creature() -> None:
    print("Testing Creature with healing capability")
    factory = HealingCreatureFactory()
    
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    # Safely check if it has the capability before calling it
    if isinstance(base, HealCapability):
        print(base.heal())
        
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, HealCapability):
        print(evolved.heal())


def test_transform_creature() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    if isinstance(base, TransformCapability):
        print(base.transform())
        print(base.attack())
        print(base.revert())
        
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, TransformCapability):
        print(evolved.transform())
        print(evolved.attack())
        print(evolved.revert())


def main() -> None:
    test_healing_creature()
    test_transform_creature()


if __name__ == "__main__":
    main()