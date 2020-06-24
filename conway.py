import math
import random
from time import sleep
print("Welcome to Conway's Game Of Life, Python Edition")
sleep(5)
cols = int(input("Enter how many columns you want the game to be: "))
rows = int(input("Enter how many rows you want the game to be: "))
def make2DArray(rows, cols):
    return [[0] * rows] * cols
def count_buddies(grid, x, y):
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            total += grid[row][col]
    total -= grid[x][y]
    print(total)
    return total
def start_algo(grid):
    next_state = make2DArray(rows, cols)
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell == 1:
                if 2 < count_buddies(grid, i, j) < 3:
                    next_state[i][j] = 1
                    print("alive \r")
                else:
                    next_state[i][j] = 0
            elif cell == 0:
                if count_buddies(grid, i, j) == 3:
                    next_state[i][j] = 1 
                else:
                    next_state[i][j] = 0
    sleep(0.25)
    for i in next_state:
        print(i)
    start_algo(next_state)
def fill2DArray(arr, rand):
    for ind, i in enumerate(arr):
        print(f"{i} \r") 
        for ind2, j in enumerate(i):
            def isRand():
                if rand == True:
                    return random.randint(0, 1) 
                elif rand == False:
                    return 0   
 
            arr[ind][ind2] = isRand()

grid = make2DArray(cols, rows)
fill2DArray(grid, False)
user_input = input("Enter 1 of the following: randomize, see templates, choose template, create my own game, more options: \n")
if user_input == "randomize":
    fill2DArray(grid, True)
sleep(2)
user_input = input("Enter 1 of the following: randomize, see templates, choose template, create my own game, start game, more options: \n")
if user_input == "start game":
    start_algo(grid) 