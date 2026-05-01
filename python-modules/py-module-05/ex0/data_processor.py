import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        """Initializes internal storage and rank counter."""
        self._queue: list[tuple[int, str]] = []
        self._rank: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        """Checks if the data is appropriate for the processor."""
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        """Processes and stores the data internally."""
        pass

    def output(self) -> tuple[int, str]:
        """Extracts the oldest data along with its rank."""
        if not self._queue:
            raise IndexError("No data left in processor.")
        return self._queue.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        # Avoid treating booleans as numbers (True == 1 in Python)
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self._queue.append((self._rank, str(item)))
                self._rank += 1
        else:
            self._queue.append((self._rank, str(data)))
            self._rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self._queue.append((self._rank, item))
                self._rank += 1
        else:
            self._queue.append((self._rank, data))
            self._rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        def is_valid_dict(d: typing.Any) -> bool:
            return (isinstance(d, dict) and
                    all(isinstance(k, str) and isinstance(v, str)
                        for k, v in d.items()))

        if is_valid_dict(data):
            return True
        if isinstance(data, list):
            return all(is_valid_dict(x) for x in data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def format_log(d: dict[str, str]) -> str:
            if 'log_level' in d and 'log_message' in d:
                return f"{d['log_level']}: {d['log_message']}"
            return str(d)

        if isinstance(data, list):
            for item in data:
                self._queue.append((self._rank, format_log(item)))
                self._rank += 1
        else:
            self._queue.append((self._rank, format_log(data)))
            self._rank += 1


if __name__ == "__main__":
    print("=== Code Nexus Data Processor ===")
    
    # --- Numeric Processor Test ---
    print("Testing Numeric Processor...")
    num_proc = NumericProcessor()
    # Passing the integer 42 to match the output expectation perfectly
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")
    
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        # This triggers the intentional mypy warning by passing a string
        num_proc.ingest("foo") 
    except ValueError as e:
        print(f"Got exception: {e}")
        
    num_data:list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_data}")
    num_proc.ingest(num_data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {rank}:\n{val}")

    # --- Text Processor Test ---
    print("Testing Text Processor...")
    txt_proc = TextProcessor()
    print(f"Trying to validate input '42': {txt_proc.validate(42)}")
    
    txt_data = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {txt_data}")
    txt_proc.ingest(txt_data)
    print("Extracting 1 value...")
    rank, val = txt_proc.output()
    print(f"Text value {rank}: {val}")

    # --- Log Processor Test ---
    print("Testing Log Processor...")
    log_proc = LogProcessor()
    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    
    log_data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!!'}
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")
