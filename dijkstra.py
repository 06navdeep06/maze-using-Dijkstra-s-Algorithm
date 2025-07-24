import heapq

def dijkstra_animated(graph, start, end):
    """
    Finds the shortest path using Dijkstra's algorithm, yielding each visited
    node for animation purposes. When the end is found, it returns the path.

    Args:
        graph (dict): An adjacency list representation of the graph.
        start (tuple): The starting node coordinates (x, y).
        end (tuple): The ending node coordinates (x, y).

    Yields:
        tuple: The coordinates of the currently visited node.

    Returns:
        list: The final shortest path, or an empty list if no path is found.
    """
    priority_queue = [(0, start, [])]
    visited = set()

    while priority_queue:
        (distance, current_node, path) = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node]

        yield current_node  # Yield the current node for visualization

        if current_node == end:
            return path  # Return the final path

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                # Assuming edge weight is always 1 for an unweighted maze grid
                heapq.heappush(priority_queue, (distance + 1, neighbor, path))

    return []  # Return an empty list if no path is found
