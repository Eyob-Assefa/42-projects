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


class Drone:
    """Represents an individual drone moving through the network.

    Attributes:
        drone_id (int): Unique identifier for the drone.
        current_location (Optional[Zone]): The zone the drone is currently in.
        path (list[Zone]): The planned route of zones to visit.
        turns_in_transit (int): Counter for turn (restricted zones).
    """

    def __init__(self, drone_id: int, start_hub: Zone) -> None:
        """Initializes the drone at the starting hub."""
        self.drone_id = drone_id
        self.current_location: Optional[Zone] = start_hub

        # The route plan provided by the algorithm
        self.path: list[Zone] = []

        # Tracks if the drone is stuck mid-air (0 means free to move)
        self.turns_in_transit: int = 0

    def set_path(self, planned_path: list[Zone]) -> None:
        """Assigns a planned route to the drone."""
        self.path = planned_path

    def get_next_destination(self) -> Optional[Zone]:
        """Looks at the path and returns the next zone it wants to move to."""
        if self.path:
            return self.path[0]
        return None

    def move(self, next_zone: Zone, is_restricted: bool = False) -> None:
        """Updates the drone's location and handles transit states."""
        if is_restricted:
            # The rules state restricted zones take 2 turns
            self.turns_in_transit = 1
            self.current_location = None
        else:
            self.current_location = next_zone
            self.turns_in_transit = 0

            # Remove the zone we just moved to from the route plan
            if self.path and self.path[0] == next_zone:
                self.path.pop(0)
