from models import Zone, Connection, Graph


class ParseError(Exception):
    """Custom exception raised for invalid file formatting."""
    pass


class Parser:
    """Handles reading and parsing the drone network file."""

    def __init__(self, filepath: str) -> None:
        """Initializes the parser with the target file."""
        self.filepath = filepath
        self.graph = Graph()
        self.raw_data: list[str] = []

    def load_file(self) -> None:
        """Reads the file safely and strips comments/empty lines."""
        try:
            with open(self.filepath, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    cleaned_line = line.strip()

                    # Ignore empty lines and comments
                    if not cleaned_line or cleaned_line.startswith('#'):
                        continue

                    self.raw_data.append(cleaned_line)

        except FileNotFoundError:
            raise ParseError(f"Error: File '{self.filepath}' was not found.")
        except Exception as e:
            # Catching other read errors
            raise ParseError(f"Unexpected error reading file: {e}")

    def extract_metadata(self, line: str) -> dict[str, str]:
        """Extracts metadata from brackets into a dictionary."""
        metadata = {}
        start_idx = line.find("[")
        end_idx = line.find("]")

        if start_idx != -1 and end_idx != -1:
            # Get the string inside the brackets
            meta_str = line[start_idx + 1: end_idx].strip()
            if meta_str:
                # Split by space, then by '='
                pairs = meta_str.split()
                for pair in pairs:
                    if "=" in pair:
                        key, value = pair.split("=", 1)
                        metadata[key] = value
        return metadata

    def parse_data(self) -> None:
        """Parses the cleaned raw data to build the graph network."""
        if not self.raw_data:
            raise ParseError("Error: The file is empty or missing data.")

        # Extract nb_drones from the first line
        first_line = self.raw_data[0]
        if not first_line.startswith("nb_drones:"):
            raise ParseError("Line 1: Must start with 'nb_drones:'.")
        try:
            self.nb_drones = int(first_line.split(":")[1].strip())
            if self.nb_drones <= 0:
                raise ValueError
        except ValueError:
            raise ParseError("Line 1: nb_drones must be a positive integer.")

        # Iterate through the rest of the lines using if/else logic
        for line_num, line in enumerate(self.raw_data[1:], start=2):
            try:
                metadata = self.extract_metadata(line)

                # Remove the metadata from the line
                core_line = line.split("[")[0].strip()

                if core_line.startswith("start_hub:") or \
                   core_line.startswith("end_hub:") or \
                   core_line.startswith("hub:"):
                    self._parse_zone(core_line, metadata, line_num)

                elif core_line.startswith("connection:"):
                    self._parse_connection(core_line, metadata, line_num)

                else:
                    raise ParseError(f"Line {line_num}: Unknown prefix.")

            except Exception as e:
                # Catching specific errors from helper methods
                raise ParseError(f"Line {line_num}: {e}")

    def _parse_zone(
        self, core_line: str, metadata: dict[str, str], line_num: int
    ) -> None:
        """Helper method to instantiate and store a Zone object."""
        # Split prefix from data (e.g., "hub:" -> "roof1 3 4")
        prefix, data_str = core_line.split(":", 1)
        parts = data_str.strip().split()

        if len(parts) != 3:
            raise ValueError("Zone definition must have name, x, and y.")

        name, x_str, y_str = parts

        if name in self.graph.nodes:
            raise ValueError(f"Zone '{name}' is already defined.")
        if "-" in name:
            raise ValueError("Zone names cannot contain dashes.")

        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            raise ValueError("Coordinates x and y must be integers.")

        # Extract specific metadata with defaults
        zone_type = metadata.get("zone", "normal")
        color = metadata.get("color", None)
        try:
            max_drones = int(metadata.get("max_drones", 1))
        except ValueError:
            raise ValueError("max_drones must be an integer.")

        # Create and store the Zone
        zone = Zone(name, (x, y), zone_type, color, max_drones)
        self.graph.nodes[name] = zone
        self.graph.adj_list[zone] = []

        # Assign to specific hub variables if needed
        if prefix == "start_hub":
            if self.graph.start_hub:
                raise ValueError("Multiple start_hubs defined.")
            self.graph.start_hub = zone
        elif prefix == "end_hub":
            if self.graph.end_hub:
                raise ValueError("Multiple end_hubs defined.")
            self.graph.end_hub = zone

    def _parse_connection(
        self, core_line: str, metadata: dict[str, str], line_num: int
    ) -> None:
        """Helper method to instantiate and store a Connection object."""
        _, data_str = core_line.split(":", 1)

        # Split "name1-name2"
        nodes = data_str.strip().split("-")
        if len(nodes) != 2:
            raise ValueError("Connection must be formatted as 'node1-node2'.")

        name1, name2 = nodes

        if name1 not in self.graph.nodes or name2 not in self.graph.nodes:
            raise ValueError("Connection references an undefined zone.")

        zone1 = self.graph.nodes[name1]
        zone2 = self.graph.nodes[name2]

        try:
            max_link = int(metadata.get("max_link_capacity", 1))
        except ValueError:
            raise ValueError("max_link_capacity must be an integer.")

        # Create connection and add to adjacency list (Bidirectional)
        conn = Connection(zone1, zone2, max_link)
        self.graph.adj_list[zone1].append(conn)

        # We also need a reverse connection since graph edges are bidirectional
        reverse_conn = Connection(zone2, zone1, max_link)
        self.graph.adj_list[zone2].append(reverse_conn)
