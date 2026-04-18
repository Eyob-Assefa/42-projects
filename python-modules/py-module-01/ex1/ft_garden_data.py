class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main() -> None:
    p1: Plant = Plant("Rose", 25, 30)
    p2: Plant = Plant("Sunflower", 80, 45)
    p3: Plant = Plant("Cactus", 15, 120)

    print("=== Garden Plant Registry ===")
    p1.show()
    p2.show()
    p3.show()


if __name__ == "__main__":
    main()
