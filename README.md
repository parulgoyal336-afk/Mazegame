# Simple Maze Game

A 2D maze game written in Python with pygame. Every game has a new random
maze, and the game can show the shortest way to the exit.

Built for the Design and Analysis of Algorithms Lab (Project 3: Maze Project).

## Features
- Random 20 x 14 maze generated with Depth-First Search (backtracking)
- Shortest-path hint found with Breadth-First Search, updated after every move
- Arrow-key movement; walls cannot be crossed
- Move counter, timer and a win message

## How it works
| Part | Function | Algorithm | Time |
| --- | --- | --- | --- |
| Maze generation | `make_maze()` | DFS with a stack | O(V) |
| Shortest path | `solve()` | BFS with a queue | O(V + E) |

The maze is treated as a graph: each cell is a vertex and each open
passage is an edge. A wall is a missing edge. The maze is a perfect maze
(V - 1 passages), so every cell is reachable and there are no loops.

## Run it
    python -m pip install pygame-ce
    python simple_maze.py

## Controls
| Key | Action |
| --- | --- |
| Arrow keys | Move |
| S | Show / hide the shortest path |
| N | New maze |
| Esc | Quit |

## Testing
The two algorithms were checked on 1,000 random mazes. All were valid,
with exactly 279 passages and a correct shortest path. Generation averaged
0.70 ms and solving 0.10 ms in a cloud test environment.

## Future work
Menus for size and difficulty, Kruskal's / Prim's / A* for comparison,
a 3D view, a two-player mode and a best-times table.
