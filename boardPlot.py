from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

class boardPlot:
    def __init__(self, width, height, board, fig, ax):
        self.width = width
        self.height = height
        self.board = board
        
        
        self.fig = fig
        self.ax = ax
        self.ax.axis([0, width, 0, height])

        self.ax.set_yticklabels([]) # remove the tick labels
        self.ax.set_xticklabels([])
        self.ax.set_xticks([]) # remove the ticks too
        self.ax.set_yticks([]) 

        for x in range(width):
            for y in range(height):
                new_patch = Rectangle([x,y], 1, 1, facecolor='blue',
                edgecolor='black', alpha=0.9, zorder=1)
                self.board.tiles[x][y].set_patch(new_patch)
                self.ax.add_patch(new_patch)
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
    
    def onclick(self, event):
        x = int(event.xdata)
        y = int(event.ydata)
        # print('you pressed', event.button, event.xdata, event.ydata)
        if str(event.button) == 'MouseButton.RIGHT':
            tile = self.board.tiles[x][y]
            if not tile.opened:
                tile.patch.set_facecolor('yellow')
        elif str(event.button) == 'MouseButton.LEFT':
            self.board.open_tile(x,y)
            tiles = self.board.recently_opened
            for tile in tiles:
                patch = tile.patch
                if tile.is_mine:
                    patch.set_facecolor('red')
                elif tile.n_neighbour_mines == 0:
                    patch.set_facecolor('0.9')            
                else:
                    patch.set_facecolor('0.9')
                    self.ax.text(tile.x + 0.5,tile.y + 0.5, 
                                str(tile.n_neighbour_mines),
                                horizontalalignment='center',
                                verticalalignment='center',
                                zorder=10)



class bogusEvent:
    def __init__(self, x, y):
        self.xdata = x
        self.ydata = y

if __name__ == "__main__":
    from board import board
    width = 9
    height = 10
    n_mines = 10
    new_board = board(width, height, n_mines)    
    new_board.print_basic_layout()

    fig = plt.figure(figsize = (width/3, height/3))
    ax = plt.gca()
    obj = boardPlot(width, height, new_board, fig, ax)

    event = bogusEvent(1.1, 0.5)
    obj.onclick(event)

    fig.savefig("test.png")