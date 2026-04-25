import sys


def ft_command_quest() -> None:
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")

    if len(sys.argv) == 1:
        print("No arguments provided!")
    else:
        args_len = len(sys.argv) - 1
        print(f"Arguments received: {args_len}")

        idx: int = 1
        for arg in sys.argv[1:]:
            print(f"Argument {idx}: {arg}")
            idx += 1

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    ft_command_quest()
