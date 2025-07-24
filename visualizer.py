import pygame

# Cardinal directions for wall checks
N, S, W, E = ('n', 's', 'w', 'e')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230) # For visited cells
YELLOW = (255, 255, 0) # For the final path

class MazeVisualizer:
    def __init__(self, maze, cell_size=20):
        pygame.init()
        self.maze = maze
        self.cell_size = cell_size
        self.width = maze.width * cell_size
        self.height = maze.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Visualizer")

    def draw_maze(self):
        """Draws the entire maze structure, including all walls."""
        self.screen.fill(WHITE)
        for cell in self.maze.cells:
            x, y = cell.x * self.cell_size, cell.y * self.cell_size
            walls = cell.walls
            
            if N in walls:
                pygame.draw.line(self.screen, BLACK, (x, y), (x + self.cell_size, y), 2)
            if S in walls:
                pygame.draw.line(self.screen, BLACK, (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
            if W in walls:
                pygame.draw.line(self.screen, BLACK, (x, y), (x, y + self.cell_size), 2)
            if E in walls:
                pygame.draw.line(self.screen, BLACK, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        pygame.display.flip()

    def highlight_cell(self, cell_coords, color):
        """Highlights a single cell with the given color."""
        x, y = cell_coords
        rect = pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

    def animate_pathfinding(self, path_generator, start_node, end_node):
        """Animates the exploration of Dijkstra's algorithm and returns the final path."""
        final_path = None
        try:
            while True:
                # Handle Pygame events to keep the window responsive
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None # Exit if window is closed

                visited_node = next(path_generator)
                if visited_node != start_node and visited_node != end_node:
                    self.highlight_cell(visited_node, LIGHT_BLUE)
                    pygame.time.wait(10) # Animation delay
        except StopIteration as e:
            final_path = e.value
        return final_path

    def draw_path(self, path):
        """Draws the solved path on the maze."""
        for i in range(len(path)):
            x, y = path[i]
            rect = pygame.Rect(x * self.cell_size + 4, y * self.cell_size + 4, self.cell_size - 8, self.cell_size - 8)
            pygame.draw.rect(self.screen, YELLOW, rect)
        pygame.display.flip()

    def run(self):
        """Keeps the Pygame window open until the user closes it."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
