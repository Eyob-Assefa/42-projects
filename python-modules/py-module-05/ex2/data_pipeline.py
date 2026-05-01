import abc
import typing


# --- 1. Base Processors (From Exercise 0) ---
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


# --- 2. The New Plugin Architecture (Exercise 2) ---

class ExportPlugin(typing.Protocol):
    """The formal Duck-Typing contract for export plugins."""
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    """A valid plugin because it perfectly matches the Protocol."""
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        # Extracts just the string value and joins them with commas
        elements: list[str] = [val for rank, val in data]
        print(", ".join(elements))


class JSONExportPlugin:
    """Another valid plugin utilizing Duck Typing."""
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        # Manually constructing a valid JSON string
        elements: list[str] = []
        for rank, val in data:
            elements.append(f'"item_{rank}": "{val}"')
            
        print("{" + ", ".join(elements) + "}")


# --- 3. The Stream Router (Updated from Exercise 1) ---

class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        item: typing.Any
        for item in stream:
            handled: bool = False
            proc: DataProcessor
            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break
            if not handled:
                print("DataStream error")
                print(f"Can't process element in stream: {item}")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        """Consumes nb items from all processors and sends to the plugin."""
        proc: DataProcessor
        for proc in self.processors:
            data_to_export: list[tuple[int, str]] = []
            
            # Try to pull 'nb' items from this specific processor
            for _ in range(nb):
                try:
                    data_to_export.append(proc.output())
                except IndexError:
                    break # Stop pulling if the processor is empty
                    
            # If we got any data from this processor, send it to the plugin
            if len(data_to_export) > 0:
                plugin.process_output(data_to_export)

    def print_processors_stats(self) -> None:
        if len(self.processors) == 0:
            print("No processor found, no data")
            return
        proc: DataProcessor
        for proc in self.processors:
            raw_name: str = type(proc).__name__
            clean_name: str = raw_name.replace("Processor", " Processor")
            print(f"{clean_name}: total {proc._rank} items processed, "
                  f"remaining {len(proc._queue)} on processor")


# --- 4. The Final Execution ---

if __name__ == "__main__":
    print("=== Code Nexus Data Pipeline ===")
    
    print("Initialize Data Stream..")
    stream = DataStream()
    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("Registering Processors")
    # We register all processors at once this time!
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch1: list[typing.Any] = [
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
    
    print("Send first batch of data on stream: ['Hello world', "
          "[3.14, 1, 2.71], [{'log_level': 'WARNING', 'log_message': "
          "'Telnet access! Use ssh instead'}, {'log_level': 'INFO', "
          "'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]")
          
    stream.process_stream(batch1)

    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    csv_plug = CSVExportPlugin()
    stream.output_pipeline(3, csv_plug)

    print("== DataStream statistics ==")
    stream.print_processors_stats()

    batch2: list[typing.Any] = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {'log_level': 'ERROR', 'log_message': '500 server crash'},
            {'log_level': 'NOTICE', 
             'log_message': 'Certificate expires in 10 days'}
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]
    
    print("Send another batch of data: "
          "[21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'], "
          "[{'log_level': 'ERROR', 'log_message': '500 server crash'}, "
          "{'log_level': 'NOTICE', 'log_message': 'Certificate expires in "
          "10 days'}], [32, 42, 64, 84, 128, 168], 'World hello']")
          
    stream.process_stream(batch2)
    
    print("== DataStream statistics ==")
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plug = JSONExportPlugin()
    stream.output_pipeline(5, json_plug)

    print("== DataStream statistics ==")
    stream.print_processors_stats()
