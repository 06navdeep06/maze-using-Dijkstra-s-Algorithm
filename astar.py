import heapq

def heuristic(a, b):
    """Calculates the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_animated(graph, start, end):
    """ 
    A* algorithm implementation that yields each visited node to visualize the process.
    """
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            yield path[::-1] # Yield the final path
            return

        yield current # Yield the current node being processed

        for neighbor in graph[current]:
            new_cost = cost_so_far[current] + 1 # Assuming cost of 1 for each step
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    yield [] # No path found

def astar(graph, start, end):
    """
    A* algorithm implementation.

    Returns:
        (list, set): A tuple containing the final path and the set of all visited nodes.
    """
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        visited.add(current)

        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1], visited

        for neighbor in graph[current]:
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return [], visited
