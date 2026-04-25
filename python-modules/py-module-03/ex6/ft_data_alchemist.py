import random


def ft_data_alchemist() -> None:
    print("=== Game Data Alchemist ===")

    players: list[str] = ['Alice', 'bob', 'Charlie', 'dylan', 'Emma',
                          'Gregory', 'john', 'kevin', 'Liam']
    print(f"Initial list of players: {players}")

    cap_all: list[str] = [p.capitalize() for p in players]
    print(f"New list with all names capitalized: {cap_all}")

    cap_only: list[str] = [p for p in players if p == p.capitalize()]
    print(f"New list of capitalized names only: {cap_only}")

    scores: dict[str, int] = {p: random.randint(0, 1000) for p in cap_all}
    print(f"Score dict: {scores}")

    vals: list[int] = [scores[k] for k in scores]
    avg: float = sum(vals) / len(vals)
    print(f"Score average is {round(avg, 2)}")

    high_scores: dict[str, int] = {
        k: scores[k] for k in scores if scores[k] > avg
    }
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    ft_data_alchemist()
