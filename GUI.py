import tkinter as tk
from tkinter import messagebox, Button
from tester import PuzzleTester
from Tiles import BFS, IDDFS, GBFS, AStar, TARGET_A, TARGET_B, PriorityQueueNode, Node, runSearchAlgorithms
from PIL import Image, ImageSequence, ImageGrab

class EightPuzzleGUI:
    def __init__(self, master):
        self.master = master
        master.title("8-Puzzle Solver")

        self.tiles = [' ', '1', '2', '3', '4', '5', '6', '7', '8']
        self.buttons = []
        # Create buttons for each algorithm
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons for each algorithm
        self.gbfs_button = Button(button_frame, text="Run GBFS", command=self.run_gbfs, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge')
        self.astar_button = Button(button_frame, text="Run A*", command=self.run_astar, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge')
        self.iddfs_button = Button(button_frame, text="Run IDDFS", command=self.run_iddfs, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge', background='lightblue', activeforeground='lightgreen', fg='black')
        self.generate_GIF_button = Button(button_frame, text="Generate GIF", command=self.generate_GIF, font=("Helvetica", 14), bg='lightblue', activebackground='lightgreen', bd=3, relief='ridge', background='lightblue', activeforeground='lightgreen', fg='black')

        # Grid the buttons onto the screen
        self.gbfs_button.grid(row=0, column=0, sticky='nsew')
        self.astar_button.grid(row=1, column=0, sticky='nsew')
        self.iddfs_button.grid(row=2, column=0, sticky='nsew')
        self.generate_GIF_button.grid(row=3, column=0, sticky='nsew')

        # Configure the rows to expand when the window is resized
        for i in range(4):
            button_frame.grid_rowconfigure(i, weight=1)

        # Configure the column to expand when the window is resized
        button_frame.grid_columnconfigure(0, weight=1)

        number_frame = tk.Frame(self.master)
        number_frame.pack(fill=tk.BOTH, expand=True)


        for i in range(9):
            btn = tk.Button(number_frame,
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
            btn.grid(row=i // 3, column=i % 3, sticky='nsew')
            self.buttons.append(btn)

        # Configure the rows and columns to expand when the window is resized
        for i in range(3):
            number_frame.grid_rowconfigure(i, weight=1)
            number_frame.grid_columnconfigure(i, weight=1)

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


    def generate_GIF(self):
        """
        take screenshots of the puzzle state at each step of the solution
        and save them to a gif file
        """


        self.shuffle_tiles()
        path = runSearchAlgorithms(BFS, self.tiles)
        # create a list to store the images
        self.images = []
        for tile in path:
            index = self.tiles.index(str(tile))
            self.move_tile(index)
            self.master.update()
            self.images.append(ImageGrab.grab(bbox=(self.master.winfo_rootx(), self.master.winfo_rooty(), self.master.winfo_rootx() + self.master.winfo_width(), self.master.winfo_rooty() + self.master.winfo_height())))
            self.master.after(500)
        # save the images to a gif file
        self.images[0].save('solution.gif', save_all=True, append_images=self.images[1:], loop=0, duration=500)







root = tk.Tk()
gui = EightPuzzleGUI(root)
root.mainloop()
