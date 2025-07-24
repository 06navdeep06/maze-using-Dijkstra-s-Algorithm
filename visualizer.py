import pygame
from maze import Maze
from dijkstra import dijkstra
from astar import astar

# --- UI Configuration ---
# Colors
BACKGROUND_COLOR = (24, 28, 36)
WALL_COLOR = (78, 88, 110)
PATH_COLOR = (34, 40, 52)
START_COLOR = (76, 175, 80)  # Green
END_COLOR = (244, 67, 54)    # Red
VISITED_COLOR = (63, 81, 181) # Indigo
SOLUTION_PATH_COLOR = (255, 235, 59) # Yellow
TEXT_COLOR = (236, 239, 244)
INFO_PANEL_COLOR = (44, 52, 68)
WATERMARK_COLOR = (255, 255, 255, 20) # White with low alpha

# Dimensions
INFO_PANEL_WIDTH = 250
MIN_MAZE_SIZE = 600

# Fonts
pygame.font.init()
try:
    TITLE_FONT = pygame.font.SysFont('Segoe UI', 32, bold=True)
    BODY_FONT = pygame.font.SysFont('Segoe UI', 16)
    WATERMARK_FONT = pygame.font.SysFont('Segoe UI', 80, bold=True)
except:
    TITLE_FONT = pygame.font.Font(None, 40)
    BODY_FONT = pygame.font.Font(None, 24)
    WATERMARK_FONT = pygame.font.Font(None, 100)

# Cardinal directions
N, S, W, E = ('n', 's', 'w', 'e')


class MazeVisualizer:
    def __init__(self, maze_width=25, maze_height=25):
        self.maze = Maze(maze_width, maze_height)
        self.cell_size = MIN_MAZE_SIZE // max(maze_width, maze_height)
        self.width = self.maze.width * self.cell_size
        self.height = self.maze.height * self.cell_size
        
        self.screen_width = self.width + INFO_PANEL_WIDTH
        self.screen_height = self.height
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pathfinding Visualizer | Navdeep")

        self.start_node = None
        self.end_node = None
        self.state = 'IDLE' # IDLE, READY_TO_RUN, FINISHED
        self.algorithm = 'Dijkstra'
        self.path_stats = {}
        self.final_path = []
        self.visited_nodes = set()

        self._reset_visualization()

    def _reset_visualization(self):
        self.start_node = None
        self.end_node = None
        self.state = 'IDLE'
        self.path_stats = {}
        self.final_path = []
        self.visited_nodes = set()
        self.maze = Maze.generate(self.maze.width, self.maze.height)
        self._draw_all()

    def _draw_all(self):
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_maze()
        self._draw_info_panel()
        pygame.display.flip()

    def _draw_maze(self):
        maze_surface = pygame.Surface((self.width, self.height))
        maze_surface.fill(PATH_COLOR)
        self._draw_background_watermark(maze_surface)

        for cell in self.maze.cells:
            x, y = cell.x * self.cell_size, cell.y * self.cell_size
            walls = cell.walls
            if N in walls: pygame.draw.line(maze_surface, WALL_COLOR, (x, y), (x + self.cell_size, y), 2)
            if S in walls: pygame.draw.line(maze_surface, WALL_COLOR, (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
            if W in walls: pygame.draw.line(maze_surface, WALL_COLOR, (x, y), (x, y + self.cell_size), 2)
            if E in walls: pygame.draw.line(maze_surface, WALL_COLOR, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        
        self.screen.blit(maze_surface, (0, 0))

    def _draw_info_panel(self):
        panel_rect = pygame.Rect(self.width, 0, INFO_PANEL_WIDTH, self.screen_height)
        pygame.draw.rect(self.screen, INFO_PANEL_COLOR, panel_rect)
        
        title_text = TITLE_FONT.render("Controls", True, TEXT_COLOR)
        self.screen.blit(title_text, (self.width + 20, 20))

        instructions = [
            "L-Click: Set Start",
            "R-Click: Set End",
            "Space: Run Algorithm",
            "T: Toggle Algorithm",
            "R: Reset Maze",
        ]
        for i, instruction in enumerate(instructions):
            text_surface = BODY_FONT.render(instruction, True, TEXT_COLOR)
            self.screen.blit(text_surface, (self.width + 20, 80 + i * 30))

        algo_text = BODY_FONT.render(f"Algorithm: {self.algorithm}", True, TEXT_COLOR)
        self.screen.blit(algo_text, (self.width + 20, 250))

        if self.state == 'FINISHED':
            stats_title = TITLE_FONT.render("Stats", True, TEXT_COLOR)
            self.screen.blit(stats_title, (self.width + 20, 320))
            
            stats = [
                f"Path Length: {self.path_stats.get('length', 'N/A')}",
                f"Nodes Visited: {self.path_stats.get('visited', 'N/A')}",
            ]
            for i, stat in enumerate(stats):
                text_surface = BODY_FONT.render(stat, True, TEXT_COLOR)
                self.screen.blit(text_surface, (self.width + 20, 380 + i * 30))

    def _draw_background_watermark(self, surface):
        watermark_text = WATERMARK_FONT.render("Navdeep", True, WATERMARK_COLOR)
        text_rect = watermark_text.get_rect(center=(self.width // 2, self.height // 2))
        surface.blit(watermark_text, text_rect)

    def highlight_cell(self, node, color):
        if not node: return
        x, y = node
        rect = pygame.Rect(x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 3, self.cell_size - 3)
        pygame.draw.rect(self.screen, color, rect)

    def draw_path(self, path):
        if not path or len(path) < 2: return
        # This animation draws the final path segment by segment
        for i in range(len(path) - 1):
            start_pos = path[i]
            end_pos = path[i+1]
            
            start_center = (start_pos[0] * self.cell_size + self.cell_size // 2, start_pos[1] * self.cell_size + self.cell_size // 2)
            end_center = (end_pos[0] * self.cell_size + self.cell_size // 2, end_pos[1] * self.cell_size + self.cell_size // 2)
            
            # Check for quit events to keep the window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            pygame.draw.line(self.screen, SOLUTION_PATH_COLOR, start_center, end_center, 4)
            pygame.display.flip()
            pygame.time.wait(25) # Delay for smooth animation

    def run(self):
        running = True
        while running:
            self._draw_all()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'FINISHED': continue
                    x, y = event.pos
                    if x < self.width:
                        grid_x, grid_y = x // self.cell_size, y // self.cell_size
                        if event.button == 1: self.start_node = (grid_x, grid_y)
                        elif event.button == 3: self.end_node = (grid_x, grid_y)
                        if self.start_node and self.end_node: self.state = 'READY_TO_RUN'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.algorithm = 'A*' if self.algorithm == 'Dijkstra' else 'Dijkstra'
                    
                    if event.key == pygame.K_SPACE and self.state == 'READY_TO_RUN':
                        graph = self.maze.to_graph()
                        # Run algorithm to get results instantly
                        if self.algorithm == 'Dijkstra':
                            final_path_result, visited_nodes_result = dijkstra(graph, self.start_node, self.end_node)
                        else:
                            final_path_result, visited_nodes_result = astar(graph, self.start_node, self.end_node)
                        
                        self.visited_nodes = visited_nodes_result
                        self.path_stats = {
                            'length': len(final_path_result) if final_path_result else 0,
                            'visited': len(self.visited_nodes)
                        }
                        self.state = 'FINISHED'

                        # Redraw visited nodes before starting the path animation
                        self._draw_all()
                        for node in self.visited_nodes:
                            if node != self.start_node and node != self.end_node:
                                self.highlight_cell(node, VISITED_COLOR)
                        self.highlight_cell(self.start_node, START_COLOR)
                        self.highlight_cell(self.end_node, END_COLOR)
                        pygame.display.flip()

                        # Animate the final path
                        if final_path_result:
                            self.draw_path(final_path_result)

                    if event.key == pygame.K_r:
                        self._reset_visualization()

            # --- Continuous Drawing ---
            for node in self.visited_nodes:
                if node != self.start_node and node != self.end_node:
                    self.highlight_cell(node, VISITED_COLOR)
            
            # The final path is now drawn via the animation, so this is no longer needed here

            self.highlight_cell(self.start_node, START_COLOR)
            self.highlight_cell(self.end_node, END_COLOR)
            
            pygame.display.flip()

        pygame.quit()
