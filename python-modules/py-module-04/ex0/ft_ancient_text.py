import sys
import typing


def ft_ancient_text() -> None:
    args_len: int = len(sys.argv)
    
    if args_len != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    file_name: str = sys.argv[1]
    
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{file_name}'")

    try:
        # Open the file in read-only mode ('r')
        file_obj: typing.IO[str] = open(file_name, 'r')
        
        # Read the entire content of the file into a string
        content: str = file_obj.read()
        
        # Print content. end="" prevents printing an artificial extra newline
        print(content, end="")
        
        # We must manually close the file to free up system resources
        file_obj.close()
        
        print(f"File '{file_name}' closed.")
        
    except Exception as e:
        # OSError automatically formats its message as "[Errno X] Message: 'file'"
        print(f"Error opening file '{file_name}': {e}")


if __name__ == "__main__":
    ft_ancient_text()