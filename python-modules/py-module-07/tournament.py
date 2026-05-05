import itertools

# Import our factories from the previous exercises
from ex0.factories import FlameFactory, AquaFactory
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory

# Import our strategies and custom error from Exercise 2
from ex2.strategies import (
    NormalStrategy, 
    AggressiveStrategy, 
    DefensiveStrategy, 
    InvalidStrategyError
)

def run_tournament(opponents: list) -> None:
    """Runs a tournament where every opponent fights every other opponent once."""
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    
    try:
        # itertools.combinations pairs up every item in the list without repeating
        for opp1, opp2 in itertools.combinations(opponents, 2):
            factory1, strategy1 = opp1
            factory2, strategy2 = opp2
            
            # Generate the base creatures for this specific battle
            fighter1 = factory1.create_base()
            fighter2 = factory2.create_base()
            
            print("* Battle *")
            print(fighter1.describe())
            print("VS.")
            print(fighter2.describe())
            print("now fight!")
            
            # The tournament doesn't care HOW they fight, it just tells the strategy to 'act'
            strategy1.act(fighter1)
            strategy2.act(fighter2)
            
    except InvalidStrategyError as e:
        # If a strategy throws an error (e.g., Flameling trying to transform), catch it and abort
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    # 1. Instantiate the factories
    flame = FlameFactory()
    aqua = AquaFactory()
    heal = HealingCreatureFactory()
    transform = TransformCreatureFactory()
    
    # 2. Instantiate the strategies
    normal = NormalStrategy()
    aggro = AggressiveStrategy()
    defensive = DefensiveStrategy()
    
    # 3. Run the exact test scenarios from the instructions
    
    print("Tournament 0 (basic)")
    print("[(Flameling+Normal), (Healing+Defensive)]")
    run_tournament([(flame, normal), (heal, defensive)])
    print()
    
    print("Tournament 1 (error)")
    print("[(Flameling+Aggressive), (Healing+Defensive)]")
    run_tournament([(flame, aggro), (heal, defensive)])
    print()
    
    print("Tournament 2 (multiple)")
    print("[(Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive)]")
    run_tournament([(aqua, normal), (heal, defensive), (transform, aggro)])


if __name__ == "__main__":
    main()
