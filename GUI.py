import tkinter as tk
from tkinter import messagebox, Button
from tester import PuzzleTester
from Tiles import BFS, IDDFS, GBFS, AStar, TARGET_A, TARGET_B, PriorityQueueNode, Node, runSearchAlgorithms

class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle Solver")

        self.tiles = [' ', '1', '2', '3', '4', '5', '6', '7', '8']
        self.buttons = []
        # Create buttons for each algorithm
        self.bfs_button = Button(root, text="Run BFS", command=self.run_bfs, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge', background='lightblue')
        self.gbfs_button = Button(root, text="Run GBFS", command=self.run_gbfs, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge')
        self.astar_button = Button(root, text="Run A*", command=self.run_astar, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge')
        self.iddfs_button = Button(root, text="Run IDDFS", command=self.run_iddfs, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge', background='lightblue', activeforeground='lightgreen', fg='black')

        # Pack the buttons onto the screen
        self.bfs_button.pack()
        self.gbfs_button.pack()
        self.astar_button.pack()
        self.iddfs_button.pack()

        frame = tk.Frame(self.master)
        frame.pack()

        for i in range(9):
            btn = tk.Button(frame,
                            text=self.tiles[i],
                            command=lambda i=i: self.move_tile(i),
                            height=2,
                            width=4,
                            font=("Helvetica", 24, 'bold'),
                            bg='lightblue',
                            activeforeground='lightgreen',
                            bd=3,
                            relief='ridge',
                            foreground='blue'
                            )
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

        self.shuffle_button = tk.Button(
            self.master, text="Shuffle", command=self.shuffle_tiles)
        self.shuffle_button.pack()

    def move_tile(self, tile_index):
        print(f"Tile {tile_index} clicked")
        # we will move the tile if it is adjacent to the empty tile
        # first we need to find the index of the empty tile
        empty_tile_index = self.tiles.index(' ')
        if tile_index == empty_tile_index:
            return
        # if the tile is in the same row or column as the empty tile
        if tile_index // 3 == empty_tile_index // 3 or tile_index % 3 == empty_tile_index % 3:
            # if the tile is one position away from the empty tile
            if abs(tile_index - empty_tile_index) == 1 or abs(tile_index - empty_tile_index) == 3:
                # swap the tiles
                self.tiles[tile_index], self.tiles[empty_tile_index] = self.tiles[empty_tile_index], self.tiles[tile_index]
                # update the button texts
                for i in range(9):
                    self.buttons[i].config(text=self.tiles[i])
                # check if the puzzle is solved
                if self.tiles == ['1', '2', '3', '4', '5', '6', '7', '8', ' ']:
                    messagebox.showinfo("Congratulations", "You solved the puzzle!")
        else:
            print("Invalid move")

    def shuffle_tiles(self):
        # use tester static method to generate a random state
        random_state = PuzzleTester.generate_solvable_state()

        for i in range(9):
            if random_state[i] == 0:
                self.tiles[i] = ' '
                self.buttons[i].config(text=' ')
            else:
                self.tiles[i] = str(random_state[i])
                self.buttons[i].config(text=random_state[i])


    def perform_path(self, path):
        print(self.tiles)
        if path is None:
            return
        else:
            for tile in path:
                index = self.tiles.index(str(tile))
                self.move_tile(index)
                self.master.update()
                self.master.after(500)


    def run_bfs(self):
        bfs_path = runSearchAlgorithms(BFS, self.tiles)
        self.perform_path(bfs_path)


    def run_gbfs(self):
        gbfs_path = runSearchAlgorithms(GBFS, self.tiles)
        self.perform_path(gbfs_path)

    def run_astar(self):
        astar_path = runSearchAlgorithms(AStar, self.tiles)
        self.perform_path(astar_path)

    def run_iddfs(self):
        iddfs_path = runSearchAlgorithms(IDDFS, self.tiles)
        self.perform_path(iddfs_path)


root = tk.Tk()
gui = EightPuzzleGUI(root)
root.mainloop()
