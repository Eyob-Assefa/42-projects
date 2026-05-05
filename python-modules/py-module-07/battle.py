from ex0 import CreatureFactory, FlameFactory, AquaFactory


def test_factory(factory: CreatureFactory) -> None:
    """Tests the creation, description, and attacks of a factory's creatures."""
    print("Testing factory")
    
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    """Pits the base creatures from two different factories against each other."""
    print("\nTesting battle")
    
    fighter1 = factory1.create_base()
    fighter2 = factory2.create_base()
    
    print(fighter1.describe())
    print("VS.")
    print(fighter2.describe())
    print("fight!")
    
    print(fighter1.attack())
    print(fighter2.attack())


def main() -> None:
    # Instantiate the factories
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    
    # Run the tests exactly as the example output requires
    test_factory(flame_factory)
    print()
    test_factory(aqua_factory)
    test_battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()