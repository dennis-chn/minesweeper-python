"""
board.py

Class file containing code for backend/internal representation of the 
minesweeper state

The 'board' class is made up of many 'boardTile' objects which represent each
tile on the board
"""

import numpy as np
import time
import random

class boardTile:
    def __init__(self, x, y):
        self.neighbours = []
        self.is_mine = False
        self.n_neighbour_mines = 0
        self.x = x
        self.y = y
        self.opened = False
    
    def set_patch(self, patch):
        self.patch = patch
    
    def set_prob(self, prob): # probability tile is mine
        self.prob = prob

class board:
    def __init__(self, width, height, n_mines):
        self.tiles = []
        self.x = width
        self.y = height
        self.n_goal = width*height - n_mines
        self.time_start = None
        
        self.completed = False

        self.recently_opened = [] # list of recently opened tiles
        self.n_tot_opened = 0
        for x in range(0, width):
            row_tiles = []
            for y in range(0, height):
                new_tile = boardTile(x, y)
                row_tiles.append(new_tile)
            self.tiles.append(row_tiles)
        self.set_mines(n_mines)
        # set all the neighbours and number of neighbour mines
        for row_tiles in self.tiles:
            for tile in row_tiles:
                x_pos = tile.x
                y_pos = tile.y
                # get all the neighbouring tiles
                for x in range(x_pos - 1, x_pos + 2):
                    for y in range(y_pos - 1, y_pos + 2):
                        if x == x_pos and y == y_pos:
                            continue
                        elif x >= self.x or x < 0 or y >= self.y or y < 0:
                            continue
                        tile.neighbours.append(self.tiles[x][y])        
    
                if tile.is_mine:
                    for neighbour_tile in tile.neighbours:
                        neighbour_tile.n_neighbour_mines += 1

    # n is the number of mines
    def set_mines(self, n):       
        tile_list_flat = [tile for row in self.tiles for tile in row]
        random.shuffle(tile_list_flat)
        if n > len(tile_list_flat):
            raise ValueError("Too many mines, not enough spaces")
        
        mine_list = tile_list_flat[0:n]

        for mine_tile in mine_list:
            mine_tile.is_mine = True
    
    # returns the number of tiles opened, -1 if tile was mine
    def open_tile(self, x, y):
        if self.time_start is None:
            self.time_start = time.time()
        self.recently_opened = []
        base_tile = self.tiles[x][y]

        if base_tile.opened:
            return 0

        base_tile.opened = True
        self.recently_opened.append(base_tile)
        n_tiles_opened = 1

        if base_tile.is_mine:
            print("Mined out")
            return -1
        elif base_tile.n_neighbour_mines == 0:
            tiles_to_open = [base_tile]
            while len(tiles_to_open) != 0:
                tile = tiles_to_open.pop()
                tile.opened = True
                for n_tile in tile.neighbours:
                    if not n_tile.opened:
                        if n_tile.n_neighbour_mines == 0:
                            tiles_to_open.append(n_tile)
                        n_tile.opened = True
                        n_tiles_opened += 1
                        self.recently_opened.append(n_tile)
        n_opened = len(self.recently_opened)
        self.n_tot_opened += n_opened
        if self.n_tot_opened == self.n_goal:
            # print("Well done!")
            # print("That took: {:.2f} seconds".format(time.time() - self.time_start))
            self.completed = True
            return time.time() - self.time_start
        elif self.n_tot_opened > self.n_goal:
            raise ValueError("Somehow opened more than we needed")
        return n_opened
        
    
    # for debugging
    def print_basic_layout(self, hide=True):
        mine_cnt = 0
        print('  ', end = '')
        for x in range(0, self.x):
            print(str(x) + '|', end='')
        print()
        for y in range(0, self.y):
            print(str(y) + '|', end='')
            for x in range(0, self.x):
                tile = self.tiles[x][y]
                if tile.opened:
                    if tile.is_mine:
                        print('x', end=' ')
                        mine_cnt += 1
                    else:
                        print(tile.n_neighbour_mines, end=' ')
                else:
                    print('-', end = ' ')
            print()
        # print("Mine count: " + str(mine_cnt))


if __name__ == "__main__":
    new_board = board(9,10,10)    
    new_board.print_basic_layout()
    while True:
        in_str = input()
        x, y = list(map(int, in_str.split(' ')))
        ret = new_board.open_tile(x, y)
        new_board.print_basic_layout()
        print("n tiles opened:" + str(ret))
        if ret == -1:
            break