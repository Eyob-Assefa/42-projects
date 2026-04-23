def garden_operations(operation_number: int) -> None:
    """Triggers different specific Python errors based on the input."""
    if operation_number == 0:
        _ = int("abc")
    elif operation_number == 1:
        _ = 1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        _ = "a" + 1  # type: ignore
    else:
        return

def test_error_types() -> None:
    """Demonstrates catching different built-in exception types."""
    print("=== Garden Error Types Demo ===")
    
    for i in range(5):
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
            if i == 4:
                print("Operation completed successfully")
        except ValueError as e:
            print(f"Caught ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"Caught ZeroDivisionError: {e}")
        except FileNotFoundError as e:
            print(f"Caught FileNotFoundError: {e}")
        except TypeError as e:
            print(f"Caught TypeError: {e}")
            
    print("All error types tested successfully!")

if __name__ == "__main__":
    test_error_types()