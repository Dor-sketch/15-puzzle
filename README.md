# 🕳️ _Matrix

Project `_Matrix` (Line-Matrix) is a comprehensive exploration of AI search algorithms, using the `8-Puzzle` problem as a case study. The program includes implementations of famouse search algorithms, such as `BFS`, `IDDFS`, `GBFS`, and `A*` search algorithms, and a custom heuristic for `A*` and `GBFS`. The program was initially developed for the **20551 Introduction to Artificial Intelligence** course at the *Open University of Israel*, and earned a perfect score of `100/100`.

<p align="center">
  <img src="/images/cpp_gui.png" title="AI8Puzzle" width="400">
  <br>
  <i>AI8Puzzle GTK GUI (C++)</i>
</p>

---

- [The 8-Puzzle Problem](#the-8-puzzle-problem)
  - [States](#states)
  - [Initial Space](#initial-space)
  - [Actions and Transition Model](#actions-and-transition-model)
  - [Goal States](#goal-states)
  - [Action cost](#action-cost)
- [Running the Program](#running-the-program)
- [Techniqul Details](#techniqul-details)
  - [Node Class](#node-class)
  - [Search Data Structures](#search-data-structures)
  - [Custom A\* and GBFS Heuristics](#custom-a-and-gbfs-heuristics)
  - [Examples](#examples)
- [Acknowledgments](#acknowledgments)
- [License](#license)

---

## The 8-Puzzle Problem

The 8-Puzzle broblem is a classic AI problem, where the goal is to move the tiles from the initial state to the target state, using the minimum number of moves. The puzzle consists of a 3x3 grid with 8 numbered tiles and one empty space. The tiles are initially arranged in a random order, and the goal is to arrange them in ascending order, with the empty space at the bottom right corner, or at the top left corner (see [wikipedia](https://en.wikipedia.org/wiki/15_puzzle)).

<p align="center">
  <img src="/images/example.gif" title="AI8Puzzle" width="400">
  <br>
    <i>Example of 8-Puzzle: Movinge tile `3` from the top left corner to its place</i>
</p>

In the following section I will describe the main components of the problem as a `search problem` in a more formal way, accoding to the book **"Artificial Intelligence: A Modern Approach"**, by *Stuart Russell and Peter Norvig*.

---

### States

```python
class State:
    def __init__(self, numbers: List[int], rows=3, cols=3):
        #...
        self.numbers = numbers
        self.rows, self.cols = rows, cols
        self.matrix = self._create_matrix(numbers, rows, cols)
    # ...
    def _create_matrix(self, numbers, rows, cols):
        return [[numbers[i * cols + j] for j in range(cols)] for i in range(rows)]
```

The `State` class is responsible for representing **a state in the world**. A state, in this specific problem, is a configuration of the puzzle. Each puzzle configuration, converting a linear array of tiles into a 2D matrix. This design choice simplifies both the visualization of the puzzle state and the implementation of moves within the puzzle space.

### Initial Space

<p align="center">
  <img src="/images/goal_state.png" title="AI8Puzzle" width="400">
  <br>
    <i>Goal state of the 8-Puzzle, GUI with `cubes` theme</i>

```python
def main():
    try:
        initial_numbers = [int(num) for num in sys.argv[3:]]
        # main constructing the first state
        initial_state = State(initial_numbers)
    except ValueError:
        print("All arguments must be integers.")
        sys.exit(1)

    print(BFS(initial_state))
    print(IDDFS(initial_state))
    print(GBFS(initial_state))
    print(AStar(initial_state))
```

The **initial state**, the one without a `parent` attribute, is defined based on the user input and starts as the tree root. The `main` function is responsible for parsing and initiating the `initial_state` instance, then it prints the result.

### Actions and Transition Model

<p align="center">
  <img src="/images/trans.png" title="AI8Puzzle" width="400">
  <br>
    <i>clicking the colored tiles will move them to the empty space</i>
</p>

```python
# ...
def generate_children(self):
    blank_x, blank_y = self.find_number_in_matrix(0)
    children = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x, y = blank_x + dx, blank_y + dy
        if 0 <= x < self.rows and 0 <= y < self.cols:
            new_numbers = self.numbers.copy()
            blank_index, new_index = blank_x * self.cols \
                + blank_y, x * self.cols + y
            new_numbers[blank_index], new_numbers[new_index] =\
                new_numbers[new_index], new_numbers[blank_index]
            children.append(State(new_numbers))
    return children
```

The **actions** and **transition mosdel** as  implemented inside the `state` class `generate_children`.

The `State` class also includes methods for generating children states, considering possible moves from the current state. This method implements the **Actions** and the **transition model**. I chose to implement them inside the `State` class to keep the idea of separated responsibility. That way, the `SearchAlgorithm` are only navigating the designed state space.

### Goal States

The problem includes two **goal states**, defined as plain `List[int]` to match the program `initial_state` input format.

```python
TARGET_A = [0, 1, 2, 3, 4, 5, 6, 7, 8]
TARGET_B = [1, 2, 3, 4, 5, 6, 7, 8, 0]
```

### Action cost

Each action performed by `generate_children` above cost 1, so `1` is the **action cost** of the problem. The `cost` is managed in the `Node` class which will be described below.

---

## Running the Program

<p align="center">
  <img src="/images/simple.png" title="AI8Puzzle" width="400">
    <img src="/images/Ayn_Hara.png" title="AI8Puzzle" width="400">
    <br>
        <i>Simple theme GUI (left) and Ayn Hara theme GUI (right)</i>
    <br>
    <img src="/images/neu_theme.jpg" title="AI8Puzzle" width="400">
    <br>
        <i>Neu theme GUI</i>
</p>



The program supports both interactive GUI and command-line interfaces. Two GUI versions are available: one implemented in Python using the `tkinter` library, and another implemented in `C++` using the `GTK` library. The Python version is more easy to use and has more features, while the C++ version offer cool visual effects and supports `CSS` styling.

- To run the C++ GUI, first make sure you have `GTK` installed. Then navigate to the directory containing `AI8Puzzle` and execute the following command in the terminal:

    ```bash
    ./make && ./main
    ```

    The program will open a window where you can interact with the puzzle. You can move the tiles by clicking on them, and choose options from the menu bar (¿)

    <p align="center">
      <img src="/images/clean2.gif" title="AI8Puzzle" width="400">
    </p>

- To run the python GUI, first make sure you have `tkinter` installed. Then navigate to the directory containing `Tiles.py` and execute the following command in the terminal:

    ```bash
    python3 GUI.py
    ```

    <p align="center">
      <img src="/images/solution_7_moves_white.gif" title="AI8Puzzle" width="240">
      <img src="/images/solution_7_moves.gif" title="AI8Puzzle" width="240">
    </p>

</p>

- To run the program in the command-line interface mode, navigate to the directory containing `Tiles.py` and execute the following command in the terminal:

    ```bash
    python3 Tiles.py <9 space-separated numbers representing the initial state>
    ```

    The program will print the results for each algorithm in the required format:

    ```bash
    <Algorithm name>
    <Explored count - numbur of expanded nodes>
    <Solution Path>
    ```

You can also use this simple tester program, which leverages the modular design of the searching algorithms to directly get the desired tests. The `PuzzleTester` class is implemented in `PuzzleTester.py` and can generate random solvable puzzles, test the algorithms, and print the results.

---

## Techniqul Details

```python
class SearchAlgorithm:
    class ExploredSet:
    # ... end of ExploredSet
    def __init__(self, initial_state, name=None):
        self.root_node = Node(initial_state)
        self.frontier = None
        self.explored = self.ExploredSet()
        self.name = name
        self.solution_node = None
```

*Note the base class of `SearchAlgorithm` init method takes the `initial_state` as the argument and turns it into the `Node` class - see below.*

For a self-exercise in python OOP programming, the search algorithms were designed as Classes, and not as simple methods. Each search algorithm is derived from the base class `SearchAlgorithm`, and includes member attributes for navigating the states space, including:

- `root_node` - instance of class Node from `main`

- `frontier` - specific derived instance of the fringe (see below)

- `ExploredSet` - Instance of a hashing table to hold the close set. `ExploredSet` is used to keep track of explored states, preventing re-exploration and aiding in efficient search. This structure helps deal efficiently with redundant paths.

---

### Node Class

The node class is responsible for representing a **node in the search tree**. The program uses 2 types of nodes: a base `Node` class and a derived `PriorityQueueNode` class.

Each `Node` instance stores the current state, the parent node, and the path cost $g(n)$. In addition, `PriorityQueueNode Class` is a specialized version of the `Node` class, used in A*and GBFS, includes a priority attribute for the heuristic value $h(n)$. The design is matching the book data structure (see section 3.2.2) for a `node`, with some improvements, such as the `PriorityQueueNode`, which includes an attribute for its priority, and an override version of the `__lt__` function ($<$). This implementation allows using the built in python data structure from module `heapq`, directly on `Nodes` instances, as will described now.

```python
class PriorityQueueNode(Node):
    def __init__(self, node):
        super().**init**(node.state, node.parent)
        # The `priority` attribute stores the estimated cost form the `PriorityQueueNode` to the target
        self.priority = None

    def __lt__(self, other):
        return self.priority < other.priority
```

Note that other methods, such as `back_track_h` and `check_h` allow for testing the heuristic, enable back-tracking, and check if the heuristic is admissible and consistent for futu future development and testing.

---

### Search Data Structures

The **Frontier Class** Acts as the fringe or the boundary between explored and unexplored states. It is a priority queue (minimum heap) in `A*` and `GBFS`, and a simple queue or stack in `BFS` and `IDDFS`, respectively. In `BFS` it's implemented as a FIFO queue, while in the `IDDFS` as a stack. In addition to its specific implementation, it is responsible for counting how many nodes expand using the `explored_count`.

The `IDDFS` also passes the `max_length` argument to its frontier and stores the `explored_count` while resetting its structures between the searches. Maximum depth was set to 40, and can be adjusted.

The **BFSFrontier and IDDFSFrontier** derived from the Frontier class, these are specialized for BFS and IDDFS algorithms, managing the order of node expansion. Note that all the frontier are implemented insdide the relevant search algorithm class, and not as a separate class. Note also for specific usage, like the `IDDFS` that uses the `max_length` argument to limit the depth of the search, and `reset_data` method to reset the structures between the searches and update the `max_length` and `explored_count`.

```python
    class BFSFrontier(Frontier):
        # BFS remove from the list start in `return self.open_list.pop(0)`
        def remove_from_frontier(self):
            if self.open_list:
                self.explored_count += 1
                return self.open_list.pop(0)
            return None
        # ...
```

```python
    class IDDFSFrontier(Frontier):
        # IDDFS removes from the back (stack) in `return self.open_list.pop()`
        def remove_from_frontier(self):
            if self.open_list:
                self.explored_count += 1
                return self.open_list.pop()
            return None
        #...
        def insert_to_frontier(self, node):
            # IDDFS als tracks the max depth in the insert method using the condidion
            if node.cost <= self.max_length+1:
                self.open_list.append(node)
```

```python
class GBFS(SearchAlgorithm):
    class GBFSFrontier(Frontier):
        # ...
        def set_priority(self, node):
            return node.my_heuristic()
```

Note GBFSfrontier sets onle the `heuristic` to the prirrity, thus $f(n)=h(n)$.

```python
class AStar(SearchAlgorithm):
    class AStarFrontier(Frontier):
        #...
        def set_priority(self, node: PriorityQueueNode):
            return node.cost + node.my_heuristic()
```

A\* frontier adds the `node.cost` to its prirrity, thus $f(n)=h(n)+g(n)$.

### Custom A* and GBFS Heuristics

The program also includes custom heuristics for A* and GBFS. The heuristics are implemented as methods inside the `PriorityQueueNode` class, and are used to calculate the estimated cost from the current state to the target state. The heuristics are used to guide the search algorithms in finding the optimal path to the target state.

To develop a consistent and admissible heuristic that differs from the traditional misplaced tiles or Manhattan distance measures, I have employed a custom modification of Cumulative Euclidean distances heuristic for A\*. It eases the problem constraints by allowing vertical moves, matching the `Relaxed Problem` technique.

For more information about the heuristics, see the `PriorityQueueNode` class in `Tiles.py`.

### Examples

Input for 30 moves solvable puzzles generated by the 'PuzzleTester':

![Alt text](/images/output_example.png)

`back_track_h` on A\* with initial_state of `[0, 1, 4, 6, 3, 2, 7, 8, 5]`

![Alt text](/images/output_example2.png)

---

## Acknowledgments

- Inspired by the book **"Artificial Intelligence: A Modern Approach"** by *Stuart Russell and Peter Norvig*.
- Thanks to the Open University of Israel for the opportunity to work on this project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
