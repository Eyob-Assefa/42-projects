class Plant:
    class Stats:
        def __init__(self) -> None:
            self.grow_calls: int = 0
            self.age_calls: int = 0
            self.show_calls: int = 0

        def display(self) -> None:
            print(f"Stats: {self.grow_calls} grow, {self.age_calls} age, "
                  f"{self.show_calls} show")

    def __init__(self, name: str, height: float, age: int) -> None:
        self.name: str = name
        self.height: float = height
        self.age_days: int = age
        self.stats = self.Stats()

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        """Utility method to check age against a year."""
        return age > 365

    @classmethod
    def create_anonymous(cls):
        """Factory method to create a default plant."""
        return cls("Unknown plant", 0.0, 0)

    def grow(self) -> None:
        self.height += 8.0
        self.stats.grow_calls += 1

    def age(self) -> None:
        self.age_days += 20
        self.stats.age_calls += 1

    def show(self) -> None:
        self.stats.show_calls += 1
        print(f"{self.name}: {self.height:.1f}cm, {self.age_days} days old")


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color: str = color
        self.is_blooming: bool = False

    def bloom(self) -> None:
        self.is_blooming = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self.is_blooming:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    class TreeStats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self.shade_calls: int = 0

        def display(self) -> None:
            super().display()
            print(f"{self.shade_calls} shade")

    def __init__(
        self, name: str, height: float, age: int, diameter: float
    ) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter: float = diameter
        self.stats: Tree.TreeStats = self.TreeStats()  # Override stats

    def produce_shade(self) -> None:
        self.stats.shade_calls += 1
        print(f"Tree {self.name} now produces a shade of "
              f"{round(self.height, 1)}cm long and"
              f"{round(self.trunk_diameter, 1)}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter:.1f}cm")


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age, color)
        self.seed_count: int = 0

    def bloom(self) -> None:
        super().bloom()
        self.seed_count = 42  # Sets seeds once bloomed

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.seed_count}")


def display_plant_stats(plant: Plant) -> None:
    """Unique function not part of any class to display analytics."""
    print(f"[statistics for {plant.name}]")
    plant.stats.display()


def main() -> None:
    print("=== Garden statistics ===")

    # --- Static Method Check ---
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    # --- Flower Analytics ---
    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_plant_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    display_plant_stats(rose)

    # --- Tree Analytics ---
    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_plant_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_plant_stats(oak)

    # --- Seed Inheritance ---
    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    display_plant_stats(sunflower)

    # --- Anonymous Class Method ---
    print("\n=== Anonymous")
    anon = Plant.create_anonymous()
    anon.show()
    display_plant_stats(anon)


if __name__ == "__main__":
    main()
