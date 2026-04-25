import sys


def process_args(args: list[str]) -> list[int]:
    result: list[int] = []

    arg: str
    for arg in args:
        try:
            result.append(int(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")

    return result


def ft_score_analytics() -> None:
    print("=== Player Score Analytics ===")

    args: list[str] = sys.argv
    args_len: int = len(args)

    if args_len == 1:
        print("No scores provided. Usage: "
              "python3 ft_score_analytics.py <score1> <score2> ...")
        return

    res_list: list[int] = process_args(args[1:])

    if len(res_list) == 0:
        print("No scores provided. "
              "Usage: python3 ft_score_analytics.py <score1> <score2> ...")
    else:
        print(f"Scores processed: {res_list}")

        total_players: int = len(res_list)
        print(f"Total players: {total_players}")

        total: int = sum(res_list)
        print(f"Total score: {total}")

        avg: float = total / total_players
        print(f"Average score: {avg}")

        high: int = max(res_list)
        print(f"High score: {high}")

        low: int = min(res_list)
        print(f"Low score: {low}")

        score_range: int = high - low
        print(f"Score range: {score_range}")


if __name__ == "__main__":
    ft_score_analytics()
