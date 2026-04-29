import sys
import typing


def ft_archive_creation() -> None:
    args_len: int = len(sys.argv)
    
    if args_len != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    file_name: str = sys.argv[1]
    
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")

    try:
        # Step 1: Read the ancient file
        file_obj: typing.IO[str] = open(file_name, 'r')
        content: str = file_obj.read()
        print(content, end="")
        
        # Ensure a clean break before the close message
        if len(content) > 0 and content[-1] != '\n':
            print()
            
        file_obj.close()
        print(f"File '{file_name}' closed.")

        # Step 2: Transform the data
        print("Transform data:")
        transformed: str = ""
        
        char: str
        for char in content:
            if char == '\n':
                transformed += "#\n"
            else:
                transformed += char
                
        # Catch the very last line if the file didn't end with a newline
        if len(content) > 0 and content[-1] != '\n':
            transformed += "#"
            
        print(transformed, end="")
        if len(transformed) > 0 and transformed[-1] != '\n':
            print() # Clean break for the input prompt

        # Step 3: Get user input and save
        new_file: str = input("Enter new file name (or empty): ")

        if new_file == "":
            print("Not saving data.")
        else:
            print(f"Saving data to '{new_file}'")
            
            # Open a new file in write mode ('w')
            out_file: typing.IO[str] = open(new_file, 'w')
            out_file.write(transformed)
            out_file.close()
            
            print(f"Data saved in file '{new_file}'.")

    except OSError as e:
        print(f"Error opening file '{file_name}': {e}")


if __name__ == "__main__":
    ft_archive_creation()
