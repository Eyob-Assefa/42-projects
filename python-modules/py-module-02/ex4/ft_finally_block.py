class GardenError(Exception):
    pass

class PlantError(GardenError):
    pass

def water_plant(plant_name: str) -> None:
    """Tries to water a plant, succeeding only if it is capitalized."""
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")

def execute_watering_cycle(plants: list[str]) -> None:
    """Runs a watering cycle using try/except/finally structure."""
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(". . ending tests and returning to main")
        return
    finally:
        print("Closing watering system")

def test_watering_system() -> None:
    """Tests the watering system with both valid and invalid data."""
    print("=== Garden Watering System ===")
    
    print("\nTesting valid plants...")
    execute_watering_cycle(["Tomato", "Lettuce", "Carrots"])
    
    print("\nTesting invalid plants...")
    execute_watering_cycle(["Tomato", "lettuce"])
    
    print("\nCleanup always happens, even with errors!")

if __name__ == "__main__":
    test_watering_system()