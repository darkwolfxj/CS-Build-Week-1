import sys
import pygame
import random
import math
from time import sleep

cell_size = int(input("Enter desired cell size (in px): \n"))
board_size = width, height = int(input("Enter desired width: \n")), int(input("Enter desired height: \n"))
print("It is advised that you keep the terminal in sight while you run pygol. From within the Game, press Enter to access the menu, press C to clear the grid, P to play/pause, R to randomize the grid and Q to quit. You can also click in the game to draw.")
sleep(3)
print("Starting game...")
dead = 0, 0, 0
alive = 0, 255, 0
max_fps = 8

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(board_size)
        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / max_fps) * 1000
        self.init_grids()
        self.paused = True
        self.game_over = False
        self.glider = [
            [1, 1, 1],
            [0, 0, 1],
            [0, 1, 0]
        ]
        self.pulsar = []
    def insert_glider(self):
        # append appropriate number of 0s to both cols and rows of glider 2D Array
        # set new 2D array to active grid
        glider_rows = len(self.glider) # rows to add to glider rows
        glider_cols = len(self.glider[0]) # zeroes to add to glider columns
        rowsToAdd = self.num_rows - glider_rows
        OsToAddToCols = self.num_cols - glider_cols
        for i in self.glider:
            for zero in range(OsToAddToCols):
                i.append(0)
        for row in range(rowsToAdd):
            self.glider.append(([0] * OsToAddToCols) + ([0] * glider_cols))
        self.active_grid = self.glider
        self.draw_grid()
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

    def count_buddies(self, grid, current_row, current_column):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                row = (current_row + i + self.num_rows) % self.num_rows
                col = (current_column + j + self.num_cols) % self.num_cols
                total += grid[row][col]
        total -= grid[current_row][current_column]
        return total
        
    def update_generation(self):
        # run algo, appply to next_grid, swap next_grid and active_grid
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                state = self.active_grid[row][col]
                neighbors = self.count_buddies(self.active_grid, row, col)
                if state == 1:
                    if neighbors == 2:
                        self.next_grid[row][col] = state
                    elif neighbors == 3:
                        self.next_grid[row][col] = state
                    else:
                        self.next_grid[row][col] = 0
                else:
                    if neighbors == 3:
                        self.next_grid[row][col] = 1
                    else:
                        self.next_grid[row][col] = state        
        self.active_grid = self.next_grid
        self.draw_grid()
        self.next_grid = []
        for row in range(self.num_rows):
            self.next_grid.append([0] * (self.num_cols))
        # self.set_grid(self.active_grid)
    
    def draw_grid(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                cell_state = alive if self.active_grid[row][col] == 1 else dead
                circle = pygame.draw.circle(self.screen, cell_state, (int(col * cell_size + cell_size/2), int(row * cell_size + cell_size/2)), int(cell_size/2), 0)
            
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
                if event.type == pygame.KEYDOWN:
                    if event.unicode == "p":
                        if self.paused:
                            print("Continuing...")
                            self.paused = False
                        else:
                            print("Pausing...")
                            self.paused = True
                            
                
                if event.type == pygame.MOUSEBUTTONUP and self.paused:
                    row = self.get_cell_row_col_from_mouse_x_y(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[0]
                    col = self.get_cell_row_col_from_mouse_x_y(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]
                    self.toggle_cell(row, col)  
                    self.draw_grid()    
                
                if event.type == pygame.KEYDOWN and self.paused:            
                    if event.unicode == "r":
                        print("Randomizing grid...")
                        self.set_grid(self.active_grid)
                        self.draw_grid()
                        continue
                    
                    elif event.unicode == "c":
                        self.set_grid(self.active_grid, 0)
                        self.draw_grid()
                        continue 
                    
                    elif event.unicode == "\r":
                        print("Accessing menu...")
                        option = input("""Options: 
To access presets, enter 1 into the terminal,
To change resolution or cell size, enter 2 in the terminal
To exit this menu, press Enter in the terminal
To quit the game, press Q \n """)
                        if option == None:
                            continue
                        if option == "1":
                            print("Presets")
                            preset = input("""Enter a preset into the terminal from the following list (or press Enter to exit this menu): 
                            glider
                            beacon
                            blinker
                            pulsar \n""")
                            if preset == None:
                                continue
                            elif preset == "glider":
                                self.insert_glider()
                            elif preset == "beacon":
                                pass
                            elif preset == "blinker":
                                pass
                            elif preset == "pulsar":
                                pass
                        if option == "2":
                            option = input("Do you want to change resolution and cell size (1), or go back (Enter)?")    
                            if option == None:
                                continue
                            elif option == "1":
                                global cell_size
                                cell_size = int(input("Enter desired cell size: "))
                                global board_size, width, height
                                board_size = width, height = int(input("Enter desired width (in px): ")), int(input("Enter desired height (in px): "))
                                self.num_cols = int(width / cell_size)
                                self.num_rows = int(height / cell_size)
                                self.init_grids()
                                self.screen = pygame.display.set_mode(board_size)
                                continue
                if event.type == pygame.KEYDOWN:
                    if event.unicode == "q":
                        print("Exiting...")
                        self.game_over = True
                        
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