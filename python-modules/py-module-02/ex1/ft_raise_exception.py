def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
        
    return temp

def test_temperature() -> None:
    print("=== Garden Temperature Checker ===")
    
    test_values = ["25", "abc", "100", "-50"]
    
    for val in test_values:
        print(f"Input data is '{val}'")
        try:
            temp = input_temperature(val)
            print(f"Temperature is now {temp}°C\n")
        except Exception as e:
            print(f"Caught input_temperature error: {e}\n")
            
    print("All tests completed - program didn't crash!")

if __name__ == "__main__":
    test_temperature()