import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        text: str = input("Enter new coordinates "
                          "as floats in format 'x,y,z': ")
        parts: list[str] = text.split(",")

        if len(parts) != 3:
            print("Invalid syntax")
            continue

        try:
            x: float = float(parts[0])
            y: float = float(parts[1])
            z: float = float(parts[2])
            return (x, y, z)
        except ValueError:
            p: str
            for p in parts:
                try:
                    float(p)
                except ValueError as err:
                    print(f"Error on parameter '{p}': {err}")
                    break


def ft_coordinate_system() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1: tuple[float, float, float] = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_c: float = math.sqrt((pos1[0]-0)**2 + (pos1[1]-0)**2 + (pos1[2]-0)**2)
    print(f"Distance to center: {round(dist_c, 4)}")

    print("Get a second set of coordinates")
    pos2: tuple[float, float, float] = get_player_pos()

    dist_two: float = math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2 +
                                (pos2[2]-pos1[2])**2)
    print(f"Distance between the 2 sets of coordinates: {round(dist_two, 4)}")


if __name__ == "__main__":
    ft_coordinate_system()
