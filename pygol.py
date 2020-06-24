import sys
import pygame
import random
import math
from time import sleep

board_size = width, height = int(input("Enter desired width: \n")), int(input("Enter desired height: \n"))
cell_size = int(input("Enter desired cell size (in px): \n"))
print("It is advised that you keep the terminal in sight while you run pygol. From within the Game, press Enter to access the menu, press C to clear the grid, P to play/pause, R to randomize the grid and Q to quit. You can also click in the game to draw.")
sleep(3)
print("Starting game...")
dead = 0, 0, 0
alive = 0, 255, 0
max_fps = 8
class Circle:
    def __init__(self, row, col, circle):
        self.row = row
        self.col = col
        self.circle = circle
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(board_size)
        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000
        self.init_grids()
        self.paused = True
        self.game_over = False
        self.glider = []
        self.circles = []
    
    def init_grids(self):
        self.num_cols = int(width / cell_size)
        self.num_rows = int(height / cell_size)
        self.active_grid = []
        for row in range(self.num_rows):
            self.active_grid.append([0] * (self.num_cols))
        self.next_grid = []
        for row in range(self.num_rows):
            self.next_grid.append([0] * (self.num_cols))
        
    def clear_screen(self):
        self.screen.fill(dead)

    def count_buddies(self, grid, x, y):
        total = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                row = (x + i + self.num_rows) % self.num_rows
                col = (y + j + self.num_cols) % self.num_cols
                total += grid[row][col]
        total -= grid[x][y]
        return total
    def update_generation(self):
        # run algo, appply to next_grid, swap next_grid and active_grid
        # self.set_grid(self.active_grid)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                state = self.active_grid[row][col]
                neighbors = self.count_buddies(self.active_grid, row, col)
                if state == 0:
                    if neighbors == 3: # reproduction
                        self.next_grid[row][col] = 1 # born
                    else:
                        self.next_grid[row][col] = 0 # stays dead
                else:
                    if neighbors < 2:
                        self.next_grid[row][col] = 0 # dies
                    if neighbors > 3: # underpopulation or overpopulation 
                        self.next_grid[row][col] = 0 # dies
                    else:
                        self.next_grid[row][col] = state # lives
        self.active_grid = self.next_grid
        # self.set_grid(self.active_grid)
    
    def draw_grid(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                cell_state = alive if self.active_grid[row][col] == 1 else dead
                circle = pygame.draw.circle(self.screen, cell_state, (int(col * cell_size + cell_size/2), int(row * cell_size + cell_size/2)), int(cell_size/2), 0)
        self.active_grid = self.next_grid
            
        pygame.display.flip()
    def set_grid(self, grid, value=None):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if value == None: 
                    grid[row][col] = random.randint(0, 1)
                else:
                    grid[row][col] = value
    def toggle_cell(self, row, col):
        state = self.active_grid[row][col]
        if state == 1:
            self.active_grid[row][col] = 0
        else:
            self.active_grid[row][col] = 1 
    def get_cell_row_col_from_mouse_x_y(self, mouse_x, mouse_y):
        row = int(math.floor(mouse_y / cell_size))
        col = int(math.floor(mouse_x / cell_size))  
        return (row, col)              
    def handle_events(self):
        for event in pygame.event.get():
                # if event is keypress of p, pause algo, toggle pause
                # if event is keypress of r, randomize grid
                # if event is keypress of q, quit
                if self.paused:
                    if event.type == pygame.MOUSEBUTTONUP:
                        row = self.get_cell_row_col_from_mouse_x_y(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[0]
                        col = self.get_cell_row_col_from_mouse_x_y(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]
                        self.toggle_cell(row, col)      
                if event.type == pygame.KEYDOWN:
                    if event.unicode == "p":
                        if self.paused:
                            print("Continuing...")
                            self.paused = False
                        else:
                            print("Pausing...")
                            self.paused = True
                    elif event.unicode == "r":
                        print("Randomizing grid...")
                        self.set_grid(self.active_grid)
                        self.draw_grid()
                        continue
                    elif event.unicode == "q":
                        print("Exiting...")
                        self.game_over = True
                    elif event.unicode == "c":
                        self.set_grid(self.active_grid, 0)
                        self.draw_grid()
                        continue 
                    elif event.unicode == "\r":
                        print("Accessinng menu...")
                        option = input("""Options: 
To access presets, enter 1 into the terminal
To exit this menu, press Enter in the terminal
To quit the game, press Q \n """)
                        if option == None:
                            continue
                        if option == "1":
                            print("Presets")
                            preset = input("Enter a preset into the terminal from the following list (or press Enter to exit this menu): ")
                            if preset == None:
                                continue
                            elif preset == "glider":
                                self.active_grid = self.glider
                            elif preset == "beacon":
                                self.active_grid = self.beacon
                            elif preset == "blinker":
                                self.active_grid = self.blinker
                            elif preset == "pulsar":
                                self.active_grid = self.pulsar

                        
                if event.type == pygame.QUIT: sys.exit()
    
    def run(self):
        while True:
            if self.game_over:
                return
            self.handle_events()
            if not self.paused:
                self.update_generation()
            self.draw_grid() 
            self.cap_framerate()
    
    def cap_framerate(self):
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now            

            
if __name__ == '__main__':
    game = Game()
    game.run()