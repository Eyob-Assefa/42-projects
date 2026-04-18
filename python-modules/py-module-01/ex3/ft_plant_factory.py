class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age_days: int = age

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, {self.age_days}"
              f" days old")


def main() -> None:
    print("=== Plant Factory Output ===")

    p1: Plant = Plant("Rose", 25.0, 30)
    p2: Plant = Plant("Oak", 200.0, 365)
    p3: Plant = Plant("Cactus", 5.0, 90)
    p4: Plant = Plant("Sunflower", 80.0, 45)
    p5: Plant = Plant("Fern", 15.0, 120)

    # Displaying each plant using the show() method
    print("Created: ", end="")
    p1.show()

    print("Created: ", end="")
    p2.show()

    print("Created: ", end="")
    p3.show()

    print("Created: ", end="")
    p4.show()

    print("Created: ", end="")
    p5.show()


if __name__ == "__main__":
    main()
