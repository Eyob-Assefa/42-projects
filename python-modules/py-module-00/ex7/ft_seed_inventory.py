#!/usr/bin/python

def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    if (unit.lower().strip() == "packets"):
        print(f"{seed_type.capitalize()} seeds: {quantity} packets available")
    elif (unit.lower().strip() == "grams"):
        print(f"{seed_type.capitalize()} seeds: {quantity} grams total")
    elif (unit.lower().strip() == "area"):
        print(
            f"{seed_type.capitalize()} seeds: "
            f"covers {quantity} square meters"
        )
