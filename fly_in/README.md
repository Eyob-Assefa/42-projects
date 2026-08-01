*This project has been created as part of the 42 curriculum by eshikur.*

## Description
This project is a Multi-Agent Pathfinding (MAPF) simulation. Its goal is to route a fleet of drones through a network of zones. All drones start at a single hub and must reach a final destination hub as quickly as possible. 

The map contains different types of zones. Some zones have strict capacity limits. Other zones are restricted and take longer to travel through. The program must find a valid path for every drone. It must avoid collisions, respect zone rules, and simulate the exact movements turn by turn.

## Instructions
The project uses standard Python and does not require heavy external libraries. A Makefile is provided to run the code easily.

To install the required testing tools (like linters), run:
```bash
make install
```

To run the simulation with a specific map file, run:

```bash
make run MAP=maps/test.txt
```

To check the code quality and types, run:

```bash
make lint
```

## Algorithm Choices and Implementation Strategy

The project is built around two main systems working together: the Pathfinder and the Simulator.

**Space-Time A* Search**
The core algorithm is a modified version of the A* search algorithm. Standard A* finds the shortest path by looking at physical distance. However, it does not understand moving obstacles. If multiple drones use standard A*, they will try to take the same path and crash.

To solve this, we use Space-Time A*. This algorithm treats time as a physical dimension. A location is no longer just "Corridor A." It is now "Corridor A at Turn 4."

When the algorithm calculates a path for the first drone, it books every step in a global Reservation Table. When the second drone calculates its path, it checks this table. If a zone is fully booked for a specific turn, the drone treats it like a wall. It will then decide to wait in place or find a different path.

**Two-Phase Simulator**
After the algorithm plans the routes, the Simulator executes them. The Simulator acts as a strict referee to prevent code errors. It uses a two-phase shift system to handle simultaneous movement.

In Phase 1, the simulation freezes time. All drones that want to move announce their departure, and their old zones are marked as empty. In Phase 2, the moving drones enter their new zones. This prevents false collisions where a drone tries to enter a room before the previous drone has fully stepped out.

## Visual Representation

The project outputs the simulation directly to the terminal. Each turn is printed on a single line.

To enhance the user experience, the visualizer reads color tags from the map file. It uses ANSI escape codes to print the zone names in their assigned colors. This makes it very easy for a human to follow specific drones as they move across different sections of the map. Drones that wait in place are hidden from the turn log to keep the output clean and easy to read.

## Example Input and Output

**Example Input Map:**

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal

```

**Expected Output:**

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal

```

## Resources

* **A* Pathfinding Concept:** Introduction to A* on geeksforgeeks and other websites plus youtube vidoes.
* **Multi-Agent Pathfinding:** Wikipedia overview of MAPF concepts and space-time reservation tables.
* **AI Usage:** An AI assistant was used as a coding assitant during this project. It helped debug normal & static typing errors (Mypy) and explained the concept of a_star, race conditions & OOP principles. It also provided guidance on formatting the terminal output using ANSI escape codes. 

```