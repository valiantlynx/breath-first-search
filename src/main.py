from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse  
from queue import Queue
import random

app = FastAPI()
 
import debugpy
debugpy.listen(("0.0.0.0", 5678))




def create_maze(rows, cols, start, end):
    # Initialize maze with walls (1)
    maze = [[1] * cols for _ in range(rows)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 1

    def dfs(x, y):
        maze[x][y] = 0  # Mark the current cell as a path (0)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + 2 * dx, y + 2 * dy
            if is_valid(new_x, new_y):
                maze[x + dx][y + dy] = 0
                dfs(new_x, new_y)

    dfs(start[0], start[1])

    # Set the start and end positions
    maze[start[0]][start[1]] = 2
    maze[end[0]][end[1]] = 3

    return maze


def bfs(maze, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = Queue()
    queue.put(start)
    parent = {start: None}

    while not queue.empty():
        current = queue.get()
        if current == end:
            break

        for dx, dy in directions:
            new_x, new_y = current[0] + dx, current[1] + dy
            if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] == 0 and (new_x, new_y) not in parent:
                queue.put((new_x, new_y))
                parent[(new_x, new_y)] = current

    # Reconstruct the path
    path = []
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


@app.get("/", response_class=HTMLResponse)
def read_root():
    rows = 11
    cols = 11
    
    #row and collum of the start and end
    start = (0, 0)
    end = (10, 10)
    
    maze = create_maze(rows, cols, start, end)
    path = bfs(maze, start, end)

    # HTML code to render the maze with animations
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css">
    </head>
    <body>
        <div class="container mx-auto p-4">
            <h1 class="text-2xl font-semibold mb-4">Maze</h1>
            <div class="flex flex-wrap" style="width: 1100px">
    """

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            tile_class = "p-1 m-0"  # No padding and no margin
            if (row, col) in path:
                tile_class += " bg-yellow-500"  # Highlight visited cells
            if maze[row][col] == 1:  # Wall
                tile_class += " bg-gray-500"
            elif maze[row][col] == 2:  # Start
                tile_class += " bg-green-500 border border-green-500"
            elif maze[row][col] == 3:  # End
                tile_class += " bg-red-500"
            else:  # Path
                tile_class += " bg-white border border-gray-300"
            
            html_content += f'<div class="{tile_class} w-24 h-24"></div>'  # Adjust dimensions

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)