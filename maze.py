import pygame
import random

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 30
CELL_SIZE = 40
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

    def draw(self, screen):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        if self.walls[0]:  # top
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:  # right
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:  # bottom
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]:  # left
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x, y), 2)

    def highlight(self, screen, color):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        pygame.draw.rect(screen, color, (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10))

    def index(self, row, col):
        if row < 0 or col < 0 or row >= ROWS or col >= COLS:
            return None
        return row * COLS + col

    def check_neighbors(self, grid):
        neighbors = []
        top_index = self.index(self.row - 1, self.col)
        right_index = self.index(self.row, self.col + 1)
        bottom_index = self.index(self.row + 1, self.col)
        left_index = self.index(self.row, self.col - 1)

        if top_index is not None and grid[top_index] and not grid[top_index].visited:
            neighbors.append(grid[top_index])
        if right_index is not None and grid[right_index] and not grid[right_index].visited:
            neighbors.append(grid[right_index])
        if bottom_index is not None and grid[bottom_index] and not grid[bottom_index].visited:
            neighbors.append(grid[bottom_index])
        if left_index is not None and grid[left_index] and not grid[left_index].visited:
            neighbors.append(grid[left_index])

        if neighbors:
            return random.choice(neighbors)
        return None

def remove_walls(current, next_cell):
    x = current.col - next_cell.col
    if x == 1:  # current is to the right of next
        current.walls[3] = False
        next_cell.walls[1] = False
    elif x == -1:  # current is to the left of next
        current.walls[1] = False
        next_cell.walls[3] = False
    y = current.row - next_cell.row
    if y == 1:  # current is below next
        current.walls[0] = False
        next_cell.walls[2] = False
    elif y == -1:  # current is above next
        current.walls[2] = False
        next_cell.walls[0] = False

def draw_grid(grid, screen):
    for cell in grid:
        cell.draw(screen)

def generate_maze():
    grid = [Cell(row, col) for row in range(ROWS) for col in range(COLS)]
    stack = []
    current = grid[0]
    while True:
        current.visited = True
        next_cell = current.check_neighbors(grid)
        if next_cell:
            next_cell.visited = True
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break
    
    # Reset visited status for next maze generation
    for cell in grid:
        cell.visited = False
    
    return grid

def move_player(direction, current_cell, grid):
    row, col = current_cell.row, current_cell.col
    if direction == 'up' and not current_cell.walls[0]:
        new_cell = grid[current_cell.index(row - 1, col)]
    elif direction == 'right' and not current_cell.walls[1]:
        new_cell = grid[current_cell.index(row, col + 1)]
    elif direction == 'down' and not current_cell.walls[2]:
        new_cell = grid[current_cell.index(row + 1, col)]
    elif direction == 'left' and not current_cell.walls[3]:
        new_cell = grid[current_cell.index(row, col - 1)]
    else:
        return current_cell
    return new_cell

def check_win(current_cell, end_cell):
    return current_cell == end_cell

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    running = True
    while running:
        grid = generate_maze()
        start_cell = grid[0]
        end_cell = grid[-1]

        # Set start and end cells
        start_cell.highlight(screen, GREEN)
        end_cell.highlight(screen, GREEN)

        current_cell = start_cell

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                   
                    if event.key == pygame.K_UP:
                        current_cell = move_player('up', current_cell, grid)
                    elif event.key == pygame.K_RIGHT:
                        current_cell = move_player('right', current_cell, grid)
                    elif event.key == pygame.K_DOWN:
                        current_cell = move_player('down', current_cell, grid)
                    elif event.key == pygame.K_LEFT:
                        current_cell = move_player('left', current_cell, grid)

            screen.fill(BLACK)
            draw_grid(grid, screen)
            start_cell.highlight(screen, RED)
            end_cell.highlight(screen, GREEN)
            current_cell.highlight(screen, BLUE)

            # Check win condition
            if check_win(current_cell, end_cell):
                font = pygame.font.Font(None, 36)
                text = font.render('Congratulations! You escaped the maze!', True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)  # Display message for 2 seconds
                break

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
