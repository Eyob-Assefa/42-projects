def input_temperature(temp_str: str) -> int:
    return int(temp_str)

def test_temperature() -> None:
    print("=== Garden Temperature ===")
    
    test_values = ["25", "abc"]
    
    for val in test_values:
        print(f"Input data is '{val}'")
        try:
            temp = input_temperature(val)
            print(f"Temperature is now {temp}°C")
        except Exception as e:
            print(f"Caught input_temperature error: {e}")
            
    print("All tests completed - program didn't crash!")

if __name__ == "__main__":
    test_temperature()