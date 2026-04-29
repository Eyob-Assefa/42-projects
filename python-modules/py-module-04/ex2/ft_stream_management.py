import sys
import typing


def ft_stream_management() -> None:
    args_len: int = len(sys.argv)
    
    if args_len != 2:
        print("Usage: ft_stream_management.py <file>")
        return

    file_name: str = sys.argv[1]
    
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")

    try:
        # Step 1: Read the ancient file
        file_obj: typing.IO[str] = open(file_name, 'r')
        content: str = file_obj.read()
        print(content, end="")
        
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
                
        if len(content) > 0 and content[-1] != '\n':
            transformed += "#"
            
        print(transformed, end="")
        if len(transformed) > 0 and transformed[-1] != '\n':
            print()

        # Step 3: Get user input using streams
        print("Enter new file name (or empty): ", end="")
        
        # Flush stdout to ensure the prompt appears before pausing for input
        sys.stdout.flush()
        
        # Read directly from standard input
        new_file_raw: str = sys.stdin.readline()
        
        # readline() includes the \n character when the user presses Enter.
        # We slice it off if it exists.
        new_file: str = new_file_raw
        if len(new_file) > 0 and new_file[-1] == '\n':
            new_file = new_file[:-1]

        if new_file == "":
            print("Not saving data.")
        else:
            print(f"Saving data to '{new_file}'")
            
            # Use a nested try-except to catch write-permission errors specifically
            try:
                out_file: typing.IO[str] = open(new_file, 'w')
                out_file.write(transformed)
                out_file.close()
                print(f"Data saved in file '{new_file}'.")
            except OSError as write_err:
                # Print to standard error stream with the required prefix
                print(f"[STDERR] Error opening file '{new_file}': {write_err}", 
                      file=sys.stderr)
                print("Data not saved.")

    except OSError as e:
        # Print to standard error stream with the required prefix
        print(f"[STDERR] Error opening file '{file_name}': {e}", 
              file=sys.stderr)


if __name__ == "__main__":
    ft_stream_management()