class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        # Default values if initial data is invalid
        self._height: float = 0.0
        self._age: int = 0

        # Use setters for validation even when initialization
        self.set_height(height)
        self.set_age(age)

    # Getters
    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    # Setters with Validation
    def set_height(self, value: float) -> None:
        if value < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = float(round(value, 1))

    def set_age(self, value: int) -> None:
        if value < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = value

    def show(self) -> None:
        rounded_height: float = round(self._height, 1)
        print(f"{self.name}: {rounded_height}cm, {self._age} days old")


def main() -> None:
    print("=== Garden Security System ===")

    # Create plant
    rose = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()
    print()

    # Valid Updates
    rose.set_height(25.0)
    print(f"Height updated: {int(rose.get_height())}cm")
    rose.set_age(30)
    print(f"Age updated: {rose.get_age()} days")
    print()

    # Invalid Updates
    rose.set_height(-10.0)
    rose.set_age(-5)
    print()

    # Final state
    print("Current state: ", end="")
    rose.show()


if __name__ == "__main__":
    main()
