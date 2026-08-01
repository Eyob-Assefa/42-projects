from models import Graph


class Visualizer:
    """Handles the colored terminal output for the simulation.

    Attributes:
        graph (Graph): The network of zones to reference for color data.
    """

    # Dictionary mapping standard color names to ANSI escape codes
    ANSI_COLORS: dict[str, str] = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "gray": "\033[90m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }

    def __init__(self, graph: Graph) -> None:
        """Initializes the visualizer with the graph data."""
        self.graph = graph

    def _get_color_code(self, color_name: str | None) -> str:
        """Retrieves the ANSI color code"""
        if not color_name:
            return self.ANSI_COLORS["reset"]

        return self.ANSI_COLORS.get(
            color_name.lower(), self.ANSI_COLORS["reset"]
            )

    def print_turn(self, turn_logs: list[str]) -> None:
        """Takes a list of drone movements and prints them with zone colors."""
        colored_output: list[str] = []

        for log in turn_logs:
            # log looks like "D1-roof1" or "D2-corridorA-tunnelB"
            parts = log.split("-", 1)

            if len(parts) == 2:
                drone_id, destination = parts

                # Check if the destination is a single zone in our graph
                if destination in self.graph.nodes:
                    target_zone = self.graph.nodes[destination]
                    color_code = self._get_color_code(target_zone.color)
                    reset_code = self.ANSI_COLORS["reset"]

                    # Format: D1-[COLOR]roof1[RESET]
                    colored_log = (
                        f"{drone_id}-{color_code}"
                        f"{destination}{reset_code}"
                    )
                    colored_output.append(colored_log)
                else:
                    # If it's a mid-air transit, print as standard text
                    colored_output.append(log)
            else:
                # Fallback for unexpected formats
                colored_output.append(log)

        # Print all simultaneous movements on one line, space-separated
        print(" ".join(colored_output))
