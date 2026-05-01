import abc
import typing


# --- Classes from Exercise 0 ---
class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self._queue: list[tuple[int, str]] = []
        self._rank: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._queue:
            raise IndexError("No data left in processor.")
        return self._queue.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
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


# --- New Code for Exercise 1 ---
class DataStream:
    def __init__(self) -> None:
        """Initializes the empty list of registered processors."""
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        """Adds a new processor to the stream."""
        self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        """Routes each item in the stream to the appropriate processor."""
        item: typing.Any
        for item in stream:
            handled: bool = False
            proc: DataProcessor
            
            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break  # Stop checking other processors once handled
                    
            if not handled:
                print("DataStream error")
                print(f"Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        """Displays the current status of all registered processors."""
        if len(self.processors) == 0:
            print("No processor found, no data")
            return

        proc: DataProcessor
        for proc in self.processors:
            # Dynamically get the class name (e.g., 'NumericProcessor')
            # and format it to match the requested output
            raw_name: str = type(proc).__name__
            clean_name: str = raw_name.replace("Processor", " Processor")
            
            total: int = proc._rank
            remain: int = len(proc._queue)
            
            print(f"{clean_name}: total {total} items processed, "
                  f"remaining {remain} on processor")


if __name__ == "__main__":
    print("=== Code Nexus Data Stream ===")
    
    stream = DataStream()
    print("Initialize Data Stream..")
    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("Registering Numeric Processor")
    num_proc = NumericProcessor()
    stream.register_processor(num_proc)

    # Creating the mixed data batch broken up for 80-char limit
    data_batch: list[typing.Any] = [
        'Hello world',
        [3.14, 1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO',
             'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]
    
    # We must print the batch exactly as requested
    print("Send first batch of data on stream: ['Hello world', "
          "[3.14, 1, 2.71], [{'log_level': 'WARNING', 'log_message': "
          "'Telnet access! Use ssh instead'}, {'log_level': 'INFO', "
          "'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]")
          
    stream.process_stream(data_batch)

    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("Registering other data processors")
    txt_proc = TextProcessor()
    log_proc = LogProcessor()
    stream.register_processor(txt_proc)
    stream.register_processor(log_proc)

    print("Send the same batch again")
    stream.process_stream(data_batch)

    print("== DataStream statistics ==>")
    stream.print_processors_stats()

    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3): 
        num_proc.output()
    for _ in range(2): 
        txt_proc.output()
    for _ in range(1): 
        log_proc.output()

    print("== DataStream statistics ==>")
    stream.print_processors_stats()