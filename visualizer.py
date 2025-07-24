import pygame
from dijkstra import dijkstra_animated

# Cardinal directions for wall checks
N, S, W, E = ('n', 's', 'w', 'e')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)

class MazeVisualizer:
    def __init__(self, maze, cell_size=20):
        pygame.init()
        self.maze = maze
        self.cell_size = cell_size
        self.width = maze.width * cell_size
        self.height = maze.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver - Click to set points, Space to solve")
        self.font = pygame.font.Font(None, 36)

        self.start_node = None
        self.end_node = None
        self.state = 'SELECT_START'

    def _get_cell_from_pos(self, pos):
        """Converts pixel coordinates to grid cell coordinates."""
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        return (col, row)

    def _draw_text(self, text):
        """Draws text instructions on the screen."""
        surface = self.font.render(text, True, BLACK)
        rect = surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(surface, rect)
        pygame.display.flip()

    def _reset_visualization(self):
        """Redraws the maze to clear any previous pathfinding visualization."""
        self.screen.fill(WHITE)
        for cell in self.maze.cells:
            x, y = cell.x * self.cell_size, cell.y * self.cell_size
            walls = cell.walls
            if N in walls: pygame.draw.line(self.screen, BLACK, (x, y), (x + self.cell_size, y), 2)
            if S in walls: pygame.draw.line(self.screen, BLACK, (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
            if W in walls: pygame.draw.line(self.screen, BLACK, (x, y), (x, y + self.cell_size), 2)
            if E in walls: pygame.draw.line(self.screen, BLACK, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        pygame.display.flip()

    def highlight_cell(self, cell_coords, color):
        """Highlights a single cell with the given color."""
        x, y = cell_coords
        rect = pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

    def draw_path(self, path):
        """Draws the solved path on the maze."""
        for (x, y) in path:
            rect = pygame.Rect(x * self.cell_size + 4, y * self.cell_size + 4, self.cell_size - 8, self.cell_size - 8)
            pygame.draw.rect(self.screen, YELLOW, rect)
        pygame.display.flip()

    def run(self):
        """Runs the main application loop for interactive maze solving."""
        running = True
        self._reset_visualization()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self._get_cell_from_pos(pygame.mouse.get_pos())
                    if self.state == 'SELECT_START':
                        self.start_node = pos
                        self.highlight_cell(self.start_node, GREEN)
                        self.state = 'SELECT_END'
                    elif self.state == 'SELECT_END':
                        self.end_node = pos
                        self.highlight_cell(self.end_node, RED)
                        self.state = 'READY_TO_RUN'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == 'READY_TO_RUN':
                        self.state = 'RUNNING'
                        graph = self.maze.to_graph()
                        path_generator = dijkstra_animated(graph, self.start_node, self.end_node)
                        
                        final_path = None
                        try:
                            while True:
                                for e in pygame.event.get(): # Keep window responsive
                                    if e.type == pygame.QUIT: running = False; break
                                if not running: break
                                
                                visited_node = next(path_generator)
                                if visited_node != self.start_node and visited_node != self.end_node:
                                    self.highlight_cell(visited_node, LIGHT_BLUE)
                                    pygame.time.wait(5)
                        except StopIteration as e:
                            final_path = e.value

                        if final_path:
                            self.draw_path(final_path)
                        
                        self.state = 'FINISHED'

                    if event.key == pygame.K_r and self.state == 'FINISHED':
                        # Reset for another run
                        self._reset_visualization()
                        self.start_node = None
                        self.end_node = None
                        self.state = 'SELECT_START'

        pygame.quit()
