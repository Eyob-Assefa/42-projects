from typing import Optional


class Zone:
    """Represents a single node (zone) in the network.

    Attributes:
        name (str): The unique identifier for the zone.
        coordinates (tuple[int, int]): The x and y position.
        zone_type (str): Type of zone (normal, restricted, etc.).
        color (Optional[str]): Optional color for visual representation.
        max_drones (int): Maximum drones allowed simultaneously.
    """

    def __init__(
        self,
        name: str,
        coordinates: tuple[int, int],
        zone_type: str = "normal",
        color: Optional[str] = None,
        max_drones: int = 1,
    ) -> None:
        """Initializes the Zone with its metadata."""
        self.name = name
        self.coordinates = coordinates
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones


class Connection:
    """Represents a bidirectional edge between two zones.

    Attributes:
        node_a (Zone): The first connected zone.
        node_b (Zone): The second connected zone.
        max_link (int): Max drones that can traverse simultaneously.
    """

    def __init__(
        self, node_a: Zone, node_b: Zone, max_link: int = 1
    ) -> None:
        """Initializes the connection between two Zone objects."""
        self.node_a = node_a
        self.node_b = node_b
        self.max_link = max_link


class Graph:
    """Manager of the network's zones and connections.

    Attributes:
        nodes (dict[str, Zone]): Maps zone names to Zone objects.
        adj_list (dict[Zone, list[Connection]]): The adjacency list.
        start_hub (Optional[Zone]): The starting zone.
        end_hub (Optional[Zone]): The destination zone.
    """

    def __init__(self) -> None:
        """Initializes an empty graph network."""
        self.nodes: dict[str, Zone] = {}
        self.adj_list: dict[Zone, list[Connection]] = {}
        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None