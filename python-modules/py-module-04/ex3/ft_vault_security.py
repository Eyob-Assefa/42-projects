import typing


def secure_archive(
    file_name: str,
    action: str = "read",
    content: str = ""
) -> tuple[bool, str]:
    """
    Safely accesses a file for reading or writing using a context manager.
    Returns a tuple: (Success_Boolean, File_Content_or_Message)
    """
    try:
        if action == "read":
            # The 'with' statement acts as a context manager
            with open(file_name, 'r') as file_obj:
                data: str = file_obj.read()
                return (True, data)
                
        elif action == "write":
            with open(file_name, 'w') as file_obj:
                file_obj.write(content)
                return (True, "Content successfully written to file")
                
        else:
            return (False, f"Unknown action requested: '{action}'")
            
    except OSError as e:
        # str(e) automatically formats to "[Errno X] Message: 'file'"
        return (False, str(e))


def test_vault_security() -> None:
    """Tests the secure_archive function matching the example output."""
    print("=== Cyber Archives Security ===")
    
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file", "read"))
    
    print("Using 'secure_archive' to read from an inaccessible file:")
    # Note: '/etc/master.passwd' is protected on macOS/BSD. 
    # If on Linux, '/etc/shadow' would trigger the exact same Errno 13.
    print(secure_archive("/etc/master.passwd", "read"))
    
    # Let's create a test file to read from first so our read succeeds
    secure_archive("test_fragment.txt", "write", 
                   "[FRAGMENT 001] Digital preservation protocols established 2087\n"
                   "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
                   "[FRAGMENT 003] Every byte saved is a victory against oblivion\n")
                   
    print("Using 'secure_archive' to read from a regular file:")
    print(secure_archive("test_fragment.txt", "read"))
    
    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", "write", "Some test content"))


if __name__ == "__main__":
    test_vault_security()
