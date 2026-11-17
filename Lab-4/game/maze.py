import random

CELL = 40

def generate_maze(cols, rows):
    """Recursive backtracker maze generation. Returns 2D grid of walls."""
    if cols <= 0 or rows <= 0:
        raise ValueError("Maze dimensions must be positive.")

    visited = [[False]*cols for _ in range(rows)]
    walls = [[[True,True,True,True] for _ in range(cols)] for _ in range(rows)]

    def neighbors(r, c):
        dirs = [(-1,0,0,1),(1,0,1,0),(0,1,2,3),(0,-1,3,2)]  # dr,dc,wall_dir,opp_dir
        result = []
        for dr,dc,wd,od in dirs:
            nr,nc = r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and not visited[nr][nc]:
                result.append((nr,nc,wd,od))
        return result

    stack = [(0,0)]
    visited[0][0] = True
    while stack:
        r,c = stack[-1]
        nbrs = neighbors(r,c)
        if nbrs:
            nr,nc,wd,od = random.choice(nbrs)
            walls[r][c][wd] = False
            walls[nr][nc][od] = False
            visited[nr][nc] = True
            stack.append((nr,nc))
        else:
            stack.pop()
    return walls

def find_path(walls, start=(0, 0), goal=None):
    """Return the shortest route through the maze as a list of (row, column)."""
    rows = len(walls)
    if rows == 0 or not walls[0]:
        return []

    cols = len(walls[0])
    if any(len(row) != cols for row in walls):
        raise ValueError("Maze rows must all have the same number of cells.")

    if goal is None:
        goal = (rows - 1, cols - 1)

    for cell in (start, goal):
        row, col = cell
        if not (0 <= row < rows and 0 <= col < cols):
            raise ValueError("Start and goal must be inside the maze.")

    directions = ((-1, 0, 0), (1, 0, 1), (0, 1, 2), (0, -1, 3))
    queue = [start]
    parent = {start: None}

    for row, col in queue:
        if (row, col) == goal:
            path = []
            cell = goal
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            return list(reversed(path))

        for dr, dc, wall_dir in directions:
            neighbor = (row + dr, col + dc)
            nr, nc = neighbor
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and not walls[row][col][wall_dir]
                and neighbor not in parent
            ):
                parent[neighbor] = (row, col)
                queue.append(neighbor)

    return []
