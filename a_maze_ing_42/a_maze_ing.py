import sys
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class MazeConfig:
    """
    Stores the configuration parameters for maze generation.
    """
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def parse_config(filepath: str) -> MazeConfig:
    """
    Reads a configuration file and parses it into a MazeConfig object.

    Args:
        filepath: The path to the configuration text file.

    Returns:
        A populated MazeConfig dataclass.
    """
    config_data = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                # Strip whitespace and ignore comments or empty lines
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue

                # Split the KEY=VALUE pair
                key, value = clean_line.split('=', 1)
                config_data[key.strip()] = value.strip()

        # convert the strings into the correct data types
        width = int(config_data['WIDTH'])
        height = int(config_data['HEIGHT'])

        # Split "1,1" into a tuple of integers (1, 1)
        entry_raw = config_data['ENTRY'].split(',')
        entry = (int(entry_raw[0]), int(entry_raw[1]))

        exit_raw = config_data['EXIT'].split(',')
        exit_coord = (int(exit_raw[0]), int(exit_raw[1]))

        output_file = config_data['OUTPUT_FILE']
        perfect = config_data['PERFECT'].lower() == 'true'

        # Handle the optional seed
        seed = int(config_data['SEED']) if 'SEED' in config_data else None

        return MazeConfig(
            width=width,
            height=height,
            entry=entry,
            exit=exit_coord,
            output_file=output_file,
            perfect=perfect,
            seed=seed
        )

    except FileNotFoundError:
        print(f"Error: Configuration file '{filepath}' not found.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing mandatory configuration key: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid value format in configuration file."
              f" Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    obj = parse_config("./config.txt")
    print(obj)
