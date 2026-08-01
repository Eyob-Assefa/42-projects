from typing import Optional
from models import Graph, Zone, Drone
from visualizer import Visualizer


class Simulator:
    """Executes the drone movements turn-by-turn, enforces simulation rules."""

    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        """Initializes the simulation environment."""
        self.graph = graph
        self.drones = drones

        # Track dynamic occupancy of zones d/t from the static Graph
        self.zone_occupancy: dict[str, int] = {
            name: 0 for name in graph.nodes.keys()
        }

        # Initialize all drones inside the start hub
        if self.graph.start_hub:
            self.zone_occupancy[self.graph.start_hub.name] = len(drones)

    def run(self, visualizer: Visualizer) -> None:
        """Main loop that ticks time forward until all drones finish."""
        while not self._all_drones_finished():
            turn_output = self._execute_turn()

            # combined movements for this turn
            if turn_output:
                visualizer.print_turn(turn_output)

    def _all_drones_finished(self) -> bool:
        """Checks if all drones have successfully reached the end_hub."""
        if not self.graph.end_hub:
            return False
        return all(
            drone.current_location == self.graph.end_hub
            for drone in self.drones
        )

    def _execute_turn(self) -> list[str]:
        """Executes a discrete turn using a two-phase moving mechanism."""
        turn_logs: list[str] = []

        # Maps a drone to its target zone and a connection string (if mid-air)
        intended_moves: dict[Drone, tuple[Zone, Optional[str]]] = {}

        # PHASE 1: Process Departures & Mid-Air Transit
        for drone in self.drones:
            # Ignore drones that have already finished
            if drone.current_location == self.graph.end_hub:
                continue

            next_zone = drone.get_next_destination()
            if not next_zone:
                continue

            # Handle drones that are mid-air toward a restricted zone
            if drone.turns_in_transit > 0:
                drone.turns_in_transit -= 1
                if drone.turns_in_transit == 0:
                    # Transit complete.
                    intended_moves[drone] = (next_zone, None)
                else:
                    # Printing the connection name for mid-air drones
                    turn_logs.append(f"D{drone.drone_id}-transit")
                continue

            # Handle standard zone departures OR waiting in place
            if drone.current_location:
                if drone.current_location != next_zone:
                    # Rule: Drones moving out of a zone free up capacity
                    if drone.current_location != self.graph.start_hub:
                        self.zone_occupancy[drone.current_location.name] -= 1

                    # Determine if heading to a restricted zone (takes 2 turns)
                    if next_zone.zone_type == "restricted":
                        intended_moves[drone] = (
                            next_zone,
                            f"{drone.current_location.name}-{next_zone.name}"
                            )
                    else:
                        intended_moves[drone] = (next_zone, None)
                else:
                    # The drone is choosing to WAIT in place
                    intended_moves[drone] = (next_zone, "WAIT")

        # PHASE 2: Process Arrivals & Enforce Capacity
        for drone, (target_zone, connection_name) in intended_moves.items():

            # Scenario A: Entering a restricted connection (Turn 1 of 2)
            if connection_name and connection_name != "WAIT":
                drone.move(target_zone, is_restricted=True)
                turn_logs.append(f"D{drone.drone_id}-{connection_name}")
                continue

            # Scenario B: Waiting in place
            if connection_name == "WAIT":
                # Execute the move but NOT log it
                drone.move(target_zone, is_restricted=False)
                continue

            # Scenario C:A zone (Normal/Priority or Turn 2 of Restricted)
            is_end_hub = (target_zone == self.graph.end_hub)
            is_start_hub = (target_zone == self.graph.start_hub)
            has_space = (
                self.zone_occupancy[target_zone.name] < target_zone.max_drones
                )

            if is_end_hub or is_start_hub or has_space:
                drone.move(target_zone, is_restricted=False)

                # The start/end hubs do not have capacity limitations
                if not is_end_hub and not is_start_hub:
                    self.zone_occupancy[target_zone.name] += 1

                turn_logs.append(f"D{drone.drone_id}-{target_zone.name}")
            else:
                # If overlapping route
                raise RuntimeError(
                    f"Collision error: Zone {target_zone.name} "
                    f"exceeded max capacity."
                )

        return turn_logs
