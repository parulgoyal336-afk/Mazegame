"""
SIMPLE MAZE GAME  -  DAA Lab Project
------------------------------------
Part 1: make_maze()  -> builds a random maze using DFS (backtracking)
Part 2: solve()      -> finds the shortest path using BFS
Part 3: main()       -> pygame window: draw maze, move player, show hint

Controls:  Arrow keys = move | S = show/hide solution | N = new maze | ESC = quit
Install :  python -m pip install pygame-ce
"""
import random
import time
from collections import deque

import pygame

# ---------- settings ----------
COLS, ROWS = 20, 14          # maze size (cells)
CELL = 40                    # size of one cell in pixels
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40   # +40 = status bar at bottom

# directions: name -> (dx, dy)
DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}


# ---------- Part 1: maze generation (DFS / backtracking) ----------
def make_maze():
    """maze[y][x] is a set of open sides, e.g. {"N", "E"} means we can walk north or east."""
    maze = [[set() for _ in range(COLS)] for _ in range(ROWS)]
    visited = {(0, 0)}
    stack = [(0, 0)]                      # start at top-left cell

    while stack:
        x, y = stack[-1]                  # look at the cell on top of the stack
        options = []                      # unvisited neighbours
        for d, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                options.append((d, nx, ny))

        if options:                       # go to a random unvisited neighbour
            d, nx, ny = random.choice(options)
            maze[y][x].add(d)             # remove the wall between the two cells
            maze[ny][nx].add(OPPOSITE[d])
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:                             # dead end -> backtrack
            stack.pop()
    return maze


# ---------- Part 2: shortest path (BFS) ----------
def solve(maze, start, goal):
    """Breadth-First Search: explores level by level, so the first time it reaches
    the goal it has used the fewest steps."""
    queue = deque([start])
    came_from = {start: None}             # remembers how we reached each cell

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for d in maze[y][x]:              # only open sides
            dx, dy = DIRS[d]
            nxt = (x + dx, y + dy)
            if nxt not in came_from:
                came_from[nxt] = (x, y)
                queue.append(nxt)

    path, cell = [], goal                 # walk backwards from goal to start
    while cell is not None:
        path.append(cell)
        cell = came_from[cell]
    return path[::-1]


# ---------- Part 3: drawing and game loop ----------
def draw(screen, font, maze, player, goal, path, show_path, moves, seconds, won):
    screen.fill((20, 22, 34))

    if show_path:                         # yellow dots = solution
        for x, y in path:
            pygame.draw.circle(screen, (255, 215, 90), (x * CELL + CELL // 2, y * CELL + CELL // 2), 5)

    gx, gy = goal                         # green square = exit
    pygame.draw.rect(screen, (90, 230, 140), (gx * CELL + 8, gy * CELL + 8, CELL - 16, CELL - 16))

    px, py = player                       # red square = player
    pygame.draw.rect(screen, (240, 80, 80), (px * CELL + 10, py * CELL + 10, CELL - 20, CELL - 20))

    for y in range(ROWS):                 # draw a wall wherever a side is NOT open
        for x in range(COLS):
            left, top = x * CELL, y * CELL
            if "N" not in maze[y][x]:
                pygame.draw.line(screen, (230, 230, 245), (left, top), (left + CELL, top), 3)
            if "S" not in maze[y][x]:
                pygame.draw.line(screen, (230, 230, 245), (left, top + CELL), (left + CELL, top + CELL), 3)
            if "W" not in maze[y][x]:
                pygame.draw.line(screen, (230, 230, 245), (left, top), (left, top + CELL), 3)
            if "E" not in maze[y][x]:
                pygame.draw.line(screen, (230, 230, 245), (left + CELL, top), (left + CELL, top + CELL), 3)

    text = "Moves: %d   Time: %ds   |   S = solution   N = new maze" % (moves, seconds)
    if won:
        text = "YOU WIN!  Moves: %d  Time: %ds   |   Press N for a new maze" % (moves, seconds)
    screen.blit(font.render(text, True, (255, 255, 255)), (10, ROWS * CELL + 10))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Maze Game")
    font = pygame.font.SysFont("arial", 20)
    clock = pygame.time.Clock()

    goal = (COLS - 1, ROWS - 1)           # exit is the bottom-right cell

    def new_game():
        maze = make_maze()
        return maze, (0, 0), solve(maze, (0, 0), goal), False, 0, time.time()

    maze, player, path, show_path, moves, start_time = new_game()
    won, seconds = False, 0

    keys = {pygame.K_UP: "N", pygame.K_DOWN: "S", pygame.K_RIGHT: "E", pygame.K_LEFT: "W"}
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_n:
                    maze, player, path, show_path, moves, start_time = new_game()
                    won = False
                elif event.key == pygame.K_s:
                    show_path = not show_path
                elif event.key in keys and not won:
                    d = keys[event.key]
                    x, y = player
                    if d in maze[y][x]:            # move only if that side is open
                        dx, dy = DIRS[d]
                        player = (x + dx, y + dy)
                        moves += 1
                        path = solve(maze, player, goal)   # hint always starts from player
                        if player == goal:
                            won = True

        if not won:
            seconds = int(time.time() - start_time)
        draw(screen, font, maze, player, goal, path, show_path, moves, seconds, won)
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
