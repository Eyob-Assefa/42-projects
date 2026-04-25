import random


def gen_player_achievements() -> set[str]:
    master: list[str] = [
        "Crafting Genius", "World Savior", "Master Explorer",
        "Collector Supreme", "Untouchable", "Boss Slayer",
        "Strategist", "Speed Runner", "Survivor",
        "Treasure Hunter", "First Steps", "Sharp Mind",
        "Unstoppable", "Hidden Path Finder"
    ]
    count: int = random.randint(3, 8)
    chosen: list[str] = random.sample(master, count)
    return set(chosen)


def ft_achievement_tracker() -> None:
    print("=== Achievement Tracker System ===")

    alice: set[str] = gen_player_achievements()
    bob: set[str] = gen_player_achievements()
    charlie: set[str] = gen_player_achievements()
    dylan: set[str] = gen_player_achievements()

    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}")

    all_dist: set[str] = set.union(alice, bob, charlie, dylan)
    print(f"All distinct achievements: {all_dist}")

    common: set[str] = set.intersection(alice, bob, charlie, dylan)
    print(f"Common achievements: {common}")

    print(f"Only Alice has: "
          f"{set.difference(alice, set.union(bob, charlie, dylan))}")
    print(f"Only Bob has: "
          f"{set.difference(bob, set.union(alice, charlie, dylan))}")
    print(f"Only Charlie has: "
          f"{set.difference(charlie, set.union(alice, bob, dylan))}")
    print(f"Only Dylan has: "
          f"{set.difference(dylan, set.union(alice, bob, charlie))}")

    print(f"Alice is missing: {set.difference(all_dist, alice)}")
    print(f"Bob is missing: {set.difference(all_dist, bob)}")
    print(f"Charlie is missing: {set.difference(all_dist, charlie)}")
    print(f"Dylan is missing: {set.difference(all_dist, dylan)}")


if __name__ == "__main__":
    ft_achievement_tracker()
