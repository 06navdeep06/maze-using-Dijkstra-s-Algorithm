import pygame
from maze import Maze
from dijkstra import dijkstra_animated
from astar import astar_animated

# Cardinal directions for wall checks
N, S, W, E = ('n', 's', 'w', 'e')

# Colors
WALL_COLOR = (20, 20, 40) # Dark blue-gray for walls
PATH_COLOR = (255, 250, 240) # Off-white for paths
START_COLOR = (60, 180, 75) # Vibrant green for the start
END_COLOR = (230, 25, 75) # Vibrant red for the end
VISITED_COLOR = (70, 130, 180) # Steel blue for visited cells
SOLUTION_COLOR = (255, 225, 25) # Bright yellow for the solution path
TEXT_COLOR = (230, 230, 230) # Light gray for text

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
        self.background_font = pygame.font.Font(None, 150)

        self.start_node = None
        self.end_node = None
        self.state = 'SELECT_START'
        self.algorithm = 'Dijkstra'  # Default algorithm

    def _get_cell_from_pos(self, pos):
        """Converts pixel coordinates to grid cell coordinates."""
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        return (col, row)

    def _draw_text(self, text):
        """Draws text instructions on the screen."""
        # Clear the area behind the text first
        text_surface = self.font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(self.width // 2, 20))
        # Add a background to the text for better readability
        background_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, text_rect.height + 10)
        pygame.draw.rect(self.screen, WALL_COLOR, background_rect)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def _reset_visualization(self):
        """Redraws the maze to clear any previous pathfinding visualization."""
        self.screen.fill(PATH_COLOR)
        self._draw_background_watermark()

        for cell in self.maze.cells:
            x, y = cell.x * self.cell_size, cell.y * self.cell_size
            walls = cell.walls
            if N in walls: pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x + self.cell_size, y), 2)
            if S in walls: pygame.draw.line(self.screen, WALL_COLOR, (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
            if W in walls: pygame.draw.line(self.screen, WALL_COLOR, (x, y), (x, y + self.cell_size), 2)
            if E in walls: pygame.draw.line(self.screen, WALL_COLOR, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        self._draw_text(f"Algorithm: {self.algorithm}")
        pygame.display.flip()

    def highlight_cell(self, cell_coords, color):
        """Highlights a single cell with the given color."""
        x, y = cell_coords
        rect = pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

    def _draw_background_watermark(self):
        """Draws a large, subtle watermark in the center of the screen."""
        watermark_surface = self.background_font.render("Navdeep", True, (200, 200, 220))
        watermark_rect = watermark_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(watermark_surface, watermark_rect)

    def draw_path(self, path):
        """Draws the solved path on the maze."""
        for (x, y) in path:
            rect = pygame.Rect(x * self.cell_size + 4, y * self.cell_size + 4, self.cell_size - 8, self.cell_size - 8)
            pygame.draw.rect(self.screen, SOLUTION_COLOR, rect)
        pygame.display.flip()

    def _regenerate_maze(self):
        """Generates a new maze and resets the visualizer state."""
        self.maze = Maze.generate(self.maze.width, self.maze.height)
        self._reset_visualization()
        self.start_node = None
        self.end_node = None
        self.state = 'SELECT_START'

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
                        self.highlight_cell(self.start_node, START_COLOR)
                        self.state = 'SELECT_END'
                    elif self.state == 'SELECT_END':
                        self.end_node = pos
                        self.highlight_cell(self.end_node, END_COLOR)
                        self.state = 'READY_TO_RUN'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.algorithm = 'A*' if self.algorithm == 'Dijkstra' else 'Dijkstra'
                        self._reset_visualization()
                        # Re-highlight start and end nodes if they exist
                        if self.start_node:
                            self.highlight_cell(self.start_node, START_COLOR)
                        if self.end_node:
                            self.highlight_cell(self.end_node, END_COLOR)

                    if event.key == pygame.K_SPACE and self.state == 'READY_TO_RUN':
                        self.state = 'RUNNING'
                        graph = self.maze.to_graph()
                        
                        if self.algorithm == 'Dijkstra':
                            path_generator = dijkstra_animated(graph, self.start_node, self.end_node)
                        else:
                            path_generator = astar_animated(graph, self.start_node, self.end_node)

                        final_path = None
                        running_animation = True
                        while running_animation:
                            for e in pygame.event.get(): # Keep window responsive
                                if e.type == pygame.QUIT: 
                                    running = False
                                    running_animation = False
                                    break
                            if not running: break

                            try:
                                visited_node = next(path_generator)
                                if isinstance(visited_node, list): # Final path received
                                    final_path = visited_node
                                    running_animation = False
                                else:
                                    if visited_node != self.start_node and visited_node != self.end_node:
                                        self.highlight_cell(visited_node, VISITED_COLOR)
                                        pygame.time.wait(10) # Adjusted timing
                            except StopIteration:
                                running_animation = False # Generator finished

                        if final_path:
                            self.draw_path(final_path)
                        
                        self.state = 'FINISHED'

                    if event.key == pygame.K_r:
                        self._regenerate_maze()

        pygame.quit()
