class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age_days: int = age

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm,"
              f"{self.age_days} days old")

    def grow(self) -> None:
        if self.name == "Rose":
            self.height += 0.8
        else:
            self.height += 0.5

    def age(self) -> None:
        self.age_days += 1


def ft_plant_growth() -> None:
    print("=== Garden Plant Growth ===")
    rose = Plant("Rose", 25.0, 30)
    initial_height = rose.height
    rose.show()

    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.grow()
        rose.age()
        rose.show()

    total_growth = rose.height - initial_height
    print(f"Growth this week: {round(total_growth, 1)}cm")


if __name__ == "__main__":
    ft_plant_growth()
