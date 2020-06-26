import sys
import pygame
import random
import math
from time import sleep

cell_size = math.ceil(float(input("Enter desired cell size (in px): \n")))
board_size = width, height = int(input("Enter desired width: \n")), int(input("Enter desired height: \n"))
width = 100 if width < 100 else width
height = 100 if height < 100 else height
board_size = width, height
dead = input("Choose a color for dead cells (red, blue, green, white, black): \n")


def color(color):
    if color == "black":
        return (0, 0, 0)
    elif color == "white":
        return (255, 255, 255)
    elif color == "red":
        return (255, 0, 0)
    elif color == "green":
        return (0, 255, 0)
    elif color == "blue":
        return (0, 0, 255)
    else:
        print("You didn't enter a color from the list. Crashing soon...")
        return
     
dead = color(dead)
alive = input("Choose a color for live cells (red, blue, green, white, black): \n")
alive = color(alive)
print("Starting game...")
print("It is advised that you keep the terminal in sight while you run pygol. From within the Game, press Enter to access the menu, press C to clear the grid, P to play/pause, R to randomize the grid and Q to quit. You can also click in the game to draw.")
sleep(3)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(board_size)
        self.last_update_completed = 0
        self.init_grids()
        self.paused = True
        self.game_over = False
        self.glider = [
            [1, 1, 1],
            [0, 0, 1],
            [0, 1, 0]
        ]
        self.explosion = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  
        ]
        self.beacon = []
        self.pulsar = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        self.blinkers = [
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]
        ]
        self.qbs = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        self.pd = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        self.count = 1
        self.death_count = 0
        self.birth_count = 0
        self.max_fps = 1
        self.random = False
        
    def insert_preset(self, preset):
        # append appropriate number of 0s to both cols and rows of glider 2D Array
        # set new 2D array to active grid
        self.preset = preset
        print(self.preset)
        rows = len(self.preset) # rows to add to glider rows
        cols = len(self.preset[0]) # zeroes to add to glider columns
        rowsToAdd = self.num_rows - rows
        OsToAddToCols = self.num_cols - cols
        for i in self.preset:
            for zero in range(OsToAddToCols):
                i.append(0)
        for row in range(rowsToAdd):
            self.preset.append(([0] * OsToAddToCols) + ([0] * cols))
        self.active_grid = self.preset
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
                row = (current_row + i + self.num_rows) % self.num_rows # counts buddies to the left and right, wrapping to the far left and far right when needed
                col = (current_column + j + self.num_cols) % self.num_cols # counts buddies to the top and bottom, wrapping to the very top and very bottom as needed.
                total += grid[row][col]
        total -= grid[current_row][current_column]
        return total
        
    def update_generation(self):
        # run algo, appply to next_grid, swap next_grid and active_grid
        self.count += 1
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
                        self.death_count += 1
                else:
                    if neighbors == 3:
                        self.next_grid[row][col] = 1
                        self.birth_count += 1
                    else:
                        self.next_grid[row][col] = state        
        if self.active_grid == self.next_grid:
            self.paused = True
            print("Game stabilized. Paused.")
            print("""
The rules of Conway's Game Of Life are simple:
1. If any live cell has three neighbors or two neighbors, it lives on in a stasis
2. If any live cell has less than 2 neighbors, it dies in underpopulation
3. If any live cell has more than 3 neighbors, it dies in overpopulation
4. If any dead cell has exactly three neighbors, it becomes alive in birth""")
        self.active_grid = self.next_grid
        self.next_grid = []
        for row in range(self.num_rows):
            self.next_grid.append([0] * (self.num_cols))
        if self.random == True:    
            global alive
            alive = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    
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
                            print("Current generation:", self.count, ", Deaths:", self.death_count, ", Births:", self.birth_count, ", Current simulation speed:", self.max_fps, "fps")
                            
                
                if event.type == pygame.MOUSEBUTTONUP and self.paused:
                    row = self.get_cell_row_col_from_mouse_x_y(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[0]
                    col = self.get_cell_row_col_from_mouse_x_y(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])[1]
                    self.toggle_cell(row, col)  
                    self.draw_grid()    
                    print("Current generation:", self.count)
                
                if event.type == pygame.KEYDOWN and self.paused:            
                    if event.unicode == "r":
                        print("Randomizing grid...")
                        self.count = 1
                        self.death_count = 0
                        self.birth_count = 0
                        self.set_grid(self.active_grid)
                        print("Current generation:", self.count)
                        self.draw_grid()
                        continue
                    
                    elif event.unicode == "c":
                        self.set_grid(self.active_grid, 0)
                        self.count = 1
                        self.birth_count = 0
                        self.death_count = 0
                        self.draw_grid()
                        continue 
                    
                    elif event.unicode == "\r":
                        print("Accessing menu...")
                        option = input(
"""Options: 
To access presets, enter 'presets' into the terminal,
To change resolution or cell size, enter 'resollution' in the terminal
To change the simulation speed, enter 'speed' into the terminal
To display the rules, enter 'rules' into the terminal
To toggle randomization of cell color for every generation, enter 'randomize' into the terminal
To exit this menu, press Enter in the terminal
To quit the game, press Q \n """)
                        if option == None:
                            continue
                        if option == "presets":
                            print("Presets")
                            preset = input(
"""Enter a preset into the terminal from the following list (or press Enter to exit this menu): 
glider
explosion
beacon
blinkers
pulsar
queen bee shuttle
pentadecathlon \n""")
                            if preset == None:
                                continue
                            elif preset == "glider":
                                self.count = 1
                                self.insert_preset(self.glider)
                                print("The current generation is:", self.count)
                            elif preset == "explosion":
                                self.insert_preset(self.explosion)
                            elif preset == "beacon":
                                self.insert_preset(self.beacon)
                            elif preset == "blinkers":
                                self.insert_preset(self.blinkers)
                            elif preset == "pulsar":
                                self.insert_preset(self.pulsar)
                            elif preset == "queen bee shuttle":
                                self.insert_preset(self.qbs)
                            elif preset == "pentadecathlon":
                                self.insert_preset(self.pd)
                        if option == "resolution":
                            global cell_size
                            cell_size = math.ceil(float(input("Enter desired cell size: ")))
                            global board_size, width, height
                            board_size = width, height = int(input("Enter desired width: \n")), int(input("Enter desired height: \n"))
                            width = 100 if width < 100 else width
                            height = 100 if height < 100 else height
                            board_size = width, height 
                            self.num_cols = int(width / cell_size)
                            self.num_rows = int(height / cell_size)
                            self.init_grids()
                            self.screen = pygame.display.set_mode(board_size)
                            continue
                        if option == "speed":
                            self.max_fps = int(input("Enter desired simulation speed (frames per second): "))
                            self.desired_milliseconds_between_updates = (1.0 / self.max_fps) * 1000
                
                        if option == "rules":
                            print("""
The rules of Conway's Game Of Life 'are simpl'e:
1. If any live cell has three neighbors or two neighbors, it lives on in a stasis
2. If any live cell has less than 2 neighbors, it dies in underpopulation
3. If any live cell has more than 3 neighbors, it dies in overpopulation
4. If any dead cell has exactly three neighbors, it becomes alive in birth""")
                        
                        if option == "randomize":
                            self.random = True if not self.random else False
                        
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
                self.draw_grid() 
                sleep(1/self.max_fps)
                self.update_generation()
                self.draw_grid() 
    
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