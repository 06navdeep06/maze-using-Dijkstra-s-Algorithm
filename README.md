# Maze Generator and Solver using Dijkstra's and A* Algorithms

This project generates a random maze and finds the shortest path from a start to an end point using Dijkstra's algorithm. The entire process is visualized in real-time using Pygame.

## Features

- **Random Maze Generation**: Creates a perfect maze using a randomized depth-first search (recursive backtracker) algorithm.
- **Graph Conversion**: The generated maze is converted into a graph data structure (adjacency list), where each cell is a node and open passages are edges.
- **Dijkstra's and A* Algorithms**: Implements both Dijkstra's and A* algorithms to find the shortest path between any two cells in the maze. You can toggle between them using the 'T' key.
- **Pygame Visualization**: Provides a rich graphical interface to view the maze and the pathfinding process.
- **Real-time Animation**:
  - The maze walls are drawn.
  - The start (green) and end (red) cells are highlighted.
  - The exploration process of Dijkstra's algorithm is animated in light blue.
  - The final shortest path is highlighted in yellow.

## How to Run

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/06navdeep06/maze-using-Dijkstra-s-Algorithm.git
    cd maze-using-Dijkstra-s-Algorithm
    ```

2.  **Install dependencies**:
    The only dependency is Pygame. You can install it using pip:
    ```bash
    pip install pygame
    ```

3.  **Run the script**:
    ```bash
    python maze.py
    ```

A Pygame window will open, displaying the maze and the animated pathfinding process.

## Credits

This project was created by **Navdeep**.
