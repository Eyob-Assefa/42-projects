import heapq
from typing import Optional, Any
from models import Graph, Zone, Drone


class Pathfinder:
    """Calculates collision-free routes for drones using Time-Space A*.

    Attributes:
        graph (Graph): The network of zones.
        drones (list[Drone]): The fleet of drones to route.
        zone_res (dict): Reservation table for zone capacities.
        link_res (dict): Reservation table for link capacities.
        max_time (int): Cutoff to prevent infinite loops.
    """

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        """Initializes the pathfinder with the graph and drones."""
        self.graph = graph
        self.drones = drones

        # Maps (zone_name, turn) -> number of drones occupying it
        self.zone_res: dict[tuple[str, int], int] = {}

        # Maps (zone_a, zone_b, turn) -> number of drones traversing it
        self.link_res: dict[tuple[str, str, int], int] = {}

        self.max_time = 10000

    def manhattan_distance(self, zone_a: Zone, zone_b: Zone) -> int:
        """Calculates the Manhattan distance between two zones."""
        x1, y1 = zone_a.coordinates
        x2, y2 = zone_b.coordinates
        return abs(x1 - x2) + abs(y1 - y2)

    def calculate_all_paths(self) -> None:
        """Calculates paths for all drones sequentially."""
        for drone in self.drones:
            if not self.graph.start_hub or not self.graph.end_hub:
                raise ValueError("Graph is missing start or end hubs.")

            # This returns the list of (Zone, Turn) tuples
            path_tuples = self._space_time_a_star(
                self.graph.start_hub, self.graph.end_hub
            )

            if not path_tuples:
                raise RuntimeError(f"No path found for Drone {drone.drone_id}")

            # Extract ONLY the Zone objects for the Drone
            zone_only_path = [zone for zone, turn in path_tuples]

            # Give the pure zones to the drone, but reserve the full tuples
            drone.set_path(zone_only_path)
            self._reserve_path(path_tuples)

    def _space_time_a_star(
        self, start: Zone, target: Zone
    ) -> Optional[list[tuple[Zone, int]]]:
        """Executes Space-Time A* search for a single drone."""
        # 1. Variable Declaration
        g_score: dict[tuple[Zone, int], int] = {}
        parent: dict[tuple[Zone, int], Optional[tuple[Zone, int]]] = {}

        # Creating state: (node, time)
        start_state = (start, 0)
        g_score[start_state] = 0
        parent[start_state] = None

        heu_start = self.manhattan_distance(start, target)

        # Priority queue: (f_score, g_score, tie_breaker, node, time)
        # Using id(start) as a tie-breaker for heapq comaprision
        pq = [(heu_start, 0, id(start), start, 0)]

        # 2. WHILE LOOP
        while pq:
            f, g_curr, _, curr, curr_t = heapq.heappop(pq)

            # Base case
            if curr == target:
                return self._reconstruct_path(parent, (curr, curr_t))

            # Ignoring stale path
            if g_curr > g_score.get((curr, curr_t), float('inf')):
                continue

            # Time limit stopping infinite search
            if curr_t > self.max_time:
                continue

            # Generating possible moves / exploring neighbors
            possible_moves: list[tuple[Zone, int, Any]] = []

            # Action A: Waiting at current place
            possible_moves.append((curr, 1, None))

            # Action B: Moving to adjacent nodes
            for conn in self.graph.adj_list.get(curr, []):
                dest = conn.node_b
                # Treat blocked zones as solid walls
                if dest.zone_type == "blocked":
                    continue
                # Restricted zones cost 2 turns
                cost = 2 if dest.zone_type == "restricted" else 1
                possible_moves.append((dest, cost, conn))

            # 3. FOR LOOP
            for v, cost, conn in possible_moves:
                next_t = curr_t + cost

                # Check Hub Exceptions: Start/End hubs ignore max_drones
                is_hub = (v == self.graph.start_hub or v == self.graph.end_hub)

                # Vertex collision (Zone Capacity Rule)
                if not is_hub:
                    occupants = self.zone_res.get((v.name, next_t), 0)
                    if occupants >= v.max_drones:
                        continue

                # Edge collision (Connection Capacity Rule)
                if conn:
                    link_occupants = self.link_res.get(
                        (curr.name, v.name, next_t), 0
                    )
                    if link_occupants >= conn.max_link:
                        continue

                # Finally neighbor relaxation
                tent_g = g_curr + cost
                next_state = (v, next_t)

                if tent_g < g_score.get(next_state, float('inf')):
                    g_score[next_state] = tent_g
                    parent[next_state] = (curr, curr_t)

                    h_n = self.manhattan_distance(v, target)
                    # Priority zones should be preferred
                    if v.zone_type == "priority":
                        h_n -= 1

                    heapq.heappush(
                        pq, (h_n + tent_g, tent_g, id(v), v, next_t)
                    )

        return None  # No path found

    def _reconstruct_path(
        self, parent: dict, current: tuple[Zone, int]
    ) -> list[tuple[Zone, int]]:
        """Reconstructs the path backwards from the goal."""
        path = []
        while current:
            path.append(current)
            current = parent.get(current)  # type: ignore
        return path[::-1]

    def _reserve_path(self, path: list[tuple[Zone, int]]) -> None:
        """Logs a finalized path into the reservation tables."""
        for i in range(len(path)):
            zone, turn = path[i]

            # 1. Reserve the Zone capacity
            state = (zone.name, turn)
            self.zone_res[state] = self.zone_res.get(state, 0) + 1

            # 2. Reserve the Connection capacity
            if i > 0:
                prev_zone, _ = path[i - 1]

                # reserve a link if the drone moved between zones
                if prev_zone != zone:
                    link_state = (prev_zone.name, zone.name, turn)
                    self.link_res[
                        link_state
                        ] = self.link_res.get(link_state, 0) + 1
