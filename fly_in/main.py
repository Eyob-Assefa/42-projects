import sys
from typing import List

from models import Drone
from parser import Parser, ParseError
from pathfinder import Pathfinder
from simulator import Simulator
from visualizer import Visualizer


def main() -> None:
    """Main execution flow for the Fly-in drone routing simulation."""
    # Ensure a map file is provided via command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_map_file>")
        sys.exit(1)

    filepath: str = sys.argv[1]

    try:
        # Phase 1: Parse the network map
        parser = Parser(filepath)
        parser.load_file()
        parser.parse_data()
        
        graph = parser.graph
        
        # Phase 2: Initialize the drone fleet at the starting hub
        if not graph.start_hub:
            raise RuntimeError("Simulation cannot start: No start_hub defined.")
            
        drones: List[Drone] = [
            Drone(i + 1, graph.start_hub) for i in range(parser.nb_drones)
        ]

        # Phase 3: Pathfinding (The Brain)
        pathfinder = Pathfinder(graph, drones)
        pathfinder.calculate_all_paths()

        # Phase 4: Simulation and Visualization (The Referee & Display)
        visualizer = Visualizer(graph)
        simulator = Simulator(graph, drones)
        
        simulator.run(visualizer)

    except ParseError as e:
        # The project requires clean error messages indicating the cause
        print(f"Parsing Error: {e}")
        sys.exit(1)
    except Exception as e:
        # Graceful exception handling to avoid raw crashes[cite: 1]
        print(f"Simulation Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()