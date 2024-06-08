"""
This program demonstrate 4 searching algorithms to solve the Tile problem
(8-Puzzle).
"""

from typing import List
from collections import deque
import heapq
import math
import sys





class State:
    """
    Represents the state of an 8-puzzle board, handling the transformation of
    a 1D list of numbers into a 2D matrix and generating possible moves.
    """
    def _is_square(self, n):
        return n == int(n ** 0.5) ** 2

    def __init__(self, numbers: List[int] = None):
        num_tiles = len(numbers)
        self.TARGET_A = [i for i in range(1, num_tiles)] + [0]
        self.TARGET_B = [0] + [i for i in range(1, num_tiles)]
        if not self._is_square(len(numbers)):
            print(numbers)
            raise ValueError("Invalid board size. Must be NxN, found " + str(len(numbers)))
        self.numbers = numbers
        self.rows, self.cols = int(math.sqrt(len(numbers))), int(math.sqrt(len(numbers)))
        self.matrix = self._create_matrix(numbers, self.rows, self.cols)

    def _is_square(self, n):
        return math.sqrt(n).is_integer()

    def _create_matrix(self, numbers, rows, cols):
        return [[numbers[i * cols + j] for j in range(cols)] for i in range(rows)]

    def find_number_in_matrix(self, number):
        for i, row in enumerate(self.matrix):
            if number in row:
                return i, row.index(number)
        return None

    def generate_children(self):
        blank_x, blank_y = self.find_number_in_matrix(0)
        children = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = blank_x + dx, blank_y + dy
            if 0 <= x < self.rows and 0 <= y < self.cols:
                new_numbers = self.numbers.copy()
                blank_index, new_index = blank_x * self.cols + blank_y, x * self.cols + y
                new_numbers[blank_index], new_numbers[new_index] = new_numbers[new_index], new_numbers[blank_index]
                children.append(State(new_numbers))
        return children

    def __repr__(self):
        return '\n'.join(['|'.join([' ' if cell == 0 else str(cell) for cell in row]) for row in self.matrix])


class Node:
    """
    Represent a node in the search tree
    """

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        # This var stores the tree length (g(n)) based on parent level + 1
        self.cost = parent.cost + 1 if parent else 0
        self.parent_op = self.get_op()  # The block moved to get to thes state

    def get_op(self):
        """
        Leverge the node structure to find operations without extra field.
        """
        if not self.parent:
            return "Start"
        child_numbers = self.state.numbers
        parent_numbers = self.parent.state.numbers
        for i in range(len(child_numbers)):
            # The block block that moved is the one that is now placed
            # where 0 was in the parent stae
            if parent_numbers[i] == 0:
                return child_numbers[i]

    def get_path(self):
        """
        Backtrack the route fron the root to the target state.
        """
        path = []
        back_node = self
        while back_node.parent:  # Exclude the root node
            path.append(back_node.parent_op)
            back_node = back_node.parent
        path.reverse()
        # cutting the root
        return path

    def __repr__(self):
        return str(self.get_path())


class PriorityQueueNode(Node):
    """
    A derrived class for A* and GBFS.
    The heuristic function implemnted here, and chosen based on serch algorithm
    """

    def __init__(self, node):
        super().__init__(node.state, node.parent)
        self.priority = None  # estimated cost to the target (h(n))

    def set_priority(self, p):
        """
        setter to update the priority attribute.
        """
        self.priority = p


    def tiles_out_of_row_and_column_heuristic(self, target: List[int]):
        dimension_size = int(len(self.state.numbers) ** 0.5)
        heuristic_value = 0
        for i, tile in enumerate(self.state.numbers):
            if tile != 0:  # Skip the blank tile
                goal_position = target.index(tile)
                current_row, current_col = divmod(i, dimension_size)
                goal_row, goal_col = divmod(goal_position, dimension_size)

                if current_row != goal_row:
                    heuristic_value += 1
                if current_col != goal_col:
                    heuristic_value += 1

        return heuristic_value

    def conflict_heuristic(self, target: List[int]):
        """
        This heuristic is based on the number of conflicts in each row and column.
        That is, the number of tiles that are in their goal row or column but are
        in the wrong position relative to each other.
        """

        dimension_size = int(len(self.state.numbers) ** 0.5)
        heuristic_value = 0
        for i, tile in enumerate(self.state.numbers):
            before_tile = heuristic_value
            if tile != 0:
                goal_position = target.index(tile)
                current_row = i // dimension_size
                current_col = i % dimension_size

                goal_row = goal_position // dimension_size
                goal_col = goal_position % dimension_size

                if before_tile == heuristic_value:
                    if goal_row != current_row or goal_col != current_col:
                        heuristic_value += self.modified_euclidean_distance(
                            current_row, current_col, goal_row, goal_col, weight=abs(current_row - goal_row) + abs(current_col - goal_col))

        return heuristic_value

    def manhattan_distance(self, target: List[int]):
        distance = 0.0
        for i, tile in enumerate(self.state.numbers):
            if tile != 0:
                goal_position = target.index(tile)
                x1, y1 = divmod(i, 3)
                x2, y2 = divmod(goal_position, 3)
                # Manhattan distance
                distance += abs(x2 - x1) + abs(y2 - y1)
        return distance

    def my_heuristic(self, target: List[int]):
        return self.conflict_heuristic()


    def modified_euclidean_distance(self, current_row, current_col, goal_row, goal_col, weight=1):
        # Basic Euclidean distance calculation
        distance = ((current_row - goal_row) ** 2 +
                    (current_col - goal_col) ** 2) ** 0.5

        # Apply the weighting factor
        return distance * weight

    def calculte_euclidean_distance_for_tile(self, current_row, current_col, goal_row, goal_col):
        return ((goal_row - current_row)**2 + (goal_col - current_col)**2)**0.5

    def calculate_euclidean_distance(self, target: List[int],
                                     dimension_size: int = 3):
        distance = 0
        for i, tile in enumerate(self.state.numbers):
            if tile != 0:
                goal_position = target.index(tile)
                x1, y1 = divmod(i, dimension_size)
                x2, y2 = divmod(goal_position, dimension_size)
                # Euclidean distance
                distance += ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        return distance

    def __lt__(self, other):
        """
        overiding the less than to use the priority values directly
        in python heap (default min heap)
        """
        return self.priority < other.priority

    def back_track_h(self, node=None):
        if node is None:
            node = self

        node_info = f"{node.state}\ng(n{node.cost}) = {node.cost}\n" + \
            f"h(n{node.cost}) = {node.my_heuristic()}\n" + \
            f"c(n{node.cost},t) = {BFS(node.state).search().cost}\n"

        if node.parent is None:
            header = "===============\nBacktrack:\n" + \
                     "g(n)  \tpath so far, aka - node depth / cost paid / level from root\n" + \
                     "h(n)  \theuristic value - estimated cost until target\n" + \
                     "c(n,t)\tshortest path fron node i to target using BFS (h*(n))\n"
            return header + "\n"
        else:
            return self.back_track_h(node.parent) + node_info + "\n"

    def check_h(self):
        self.is_admissible()
        self.is_consistent()
        print(self.back_track_h())

    def is_admissible(self):
        true_cost = BFS(self.state).search().cost
        if self.my_heuristic() > true_cost:
            print(
                f"Not admissibe: h(n) = {self.my_heuristic()} > {true_cost}")

    def is_consistent(self):
        true_cost = BFS(self.state).search().cost
        childrens = self.state.generate_children()
        for child in childrens:
            child_node = PriorityQueueNode(Node(child, self))
            # check if estimated cost + prev cost bigger than true cost
            if true_cost > child_node.cost + child_node.my_heuristic():
                print(
                    f"Not consistent (monotonic): {true_cost} > {child_node.cost} + {child_node.my_heuristic()}")
                break


class Frontier:
    """
    Base class for open nodes data structure - fringe.
    The default type of the structure is a heap.
    In uninformed algorithms the type changes to list (for Stack and FIFO)
    """

    def __init__(self, initial_node, max_length=None, previous_count: int = 0, is_heap=True):
        self.open_list = []
        if not is_heap:
            self.open_list = deque()
        self.explored_count = previous_count
        self.max_length = max_length
        self.insert_to_frontier(initial_node)

    def set_priority(self, node):
        """
        This method is overriden in the derrived class based on the searching
        algorithm.
        """
        return 0

    def remove_from_frontier(self):
        if self.open_list:
            self.explored_count += 1
            return heapq.heappop(self.open_list)
        return None

    def insert_to_frontier(self, node):
        pq_node = PriorityQueueNode(node)
        pq_node.set_priority(self.set_priority(pq_node))
        heapq.heappush(self.open_list, pq_node)  # Corrected insertion

    def __repr__(self):
        return str(self.explored_count)


# ==================================================
class SearchAlgorithm:
    """
    Base class
    """
    class ExploredSet:
        """
        List of closed states, using hashing. closed_set
        """

        def __init__(self):
            self.table = {}

        def hash_function(self, numbers):
            """
            Generate uniqe key using the blocks positions
            """
            key = 0
            for i, number in enumerate(numbers):
                try:
                    key += number * (10 ** i)
                except:
                    print(numbers)
                    print(i)
                    print(number)
                    raise ValueError ("Invalid number")
            return key

        def find(self, state):
            key = self.hash_function(state.numbers)
            return key in self.table

        def insert(self, state):
            key = self.hash_function(state.numbers)
            if key not in self.table:
                self.table[key] = state

        def __contains__(self, state):
            return state in self.table

        def __len__(self):
            return len(self.table)

    def __init__(self, initial_state, name=None):
        self.root_node = Node(initial_state)
        self.frontier = None
        self.explored = self.ExploredSet()
        self.name = name
        self.solution_node = None

    def search(self):
        """
        Dummy decleration to be overriden
        """
        return 0

    def is_target(self, state):
        return state.numbers == state.TARGET_A or \
            state.numbers == state.TARGET_B

    def __repr__(self):
        self.solution_node = self.search()
        if self.solution_node == 0:
            self.solution_node = "No Solution Found"
        return f"{self.name}\n{self.frontier}\n{self.solution_node}"


class BFS(SearchAlgorithm):
    class BFSFrontier(Frontier):
        """
        BFS Fronties is implemented as a FIFO queu
        """

        def __init__(self, initial_node: Node):
            super().__init__(initial_node)
            # Queue is initialized with the root node

        def remove_from_frontier(self):
            if self.open_list:
                # For BFS, we remove from the front of the list (queue behavior)
                self.explored_count += 1
                return self.open_list.popleft()
            return None

        def insert_to_frontier(self, node):
            # Insert the node to the frontier
            self.open_list.append(node)

    def __init__(self, initial_state):
        super().__init__(initial_state, "BFS")
        self.frontier = self.BFSFrontier(self.root_node)

    def search(self):
        while self.frontier.open_list:
            current_node = self.frontier.remove_from_frontier()
            if self.is_target(current_node.state):
                return current_node

            for child_state in current_node.state.generate_children():
                if not self.explored.find(child_state):
                    child_node = Node(child_state, current_node)
                    self.frontier.insert_to_frontier(child_node)

            self.explored.insert(current_node.state)

        return None


class IDDFS(SearchAlgorithm):
    class IDDFSFrontier(Frontier):
        """
        IDDFS Frontier is implemented as a stack (LIFO) with a limited size.
        """

        def __init__(self, initial_node: Node, max_length: int, previous_count: int = 0):
            super().__init__(initial_node, max_length, previous_count)

        def remove_from_frontier(self):
            if self.open_list:
                self.explored_count += 1
                return self.open_list.popleft()

            return None

        def insert_to_frontier(self, node):
            # Check if adding this node will exceed the maximum length
            if node.cost <= self.max_length+1:
                self.open_list.append(node)

    def __init__(self, initial_state):
        super().__init__(initial_state, "IDDFS")
        self.initial_state = initial_state
        self.l = 0
        self.frontier = self.IDDFSFrontier(
            initial_node=self.root_node, max_length=self.l)

    def search(self):
        while self.l < 40:
            while self.frontier.open_list:
                current_node = self.frontier.remove_from_frontier()
                if self.is_target(current_node.state):
                    return current_node

                for child_state in current_node.state.generate_children():
                    if not self.explored.find(child_state):
                        child_node = Node(child_state, current_node)
                        self.frontier.insert_to_frontier(child_node)
                self.explored.insert(current_node.state)
            self.reset_data()

        return None

    def reset_data(self):
        """
        avoid python recursion limit by reset data
        """
        self.l += 1
        self.root_node = Node(self.initial_state)
        prev_count = self.frontier.explored_count
        self.frontier = self.IDDFSFrontier(
            initial_node=self.root_node, max_length=self.l, previous_count=prev_count)
        self.explored = self.ExploredSet()


class GBFS(SearchAlgorithm):
    """
    Represent the Greedy Best-First search
    """
    class GBFSFrontier(Frontier):
        """
        Derived data structer for overidden priority function
        """

        def __init__(self, initial_node):
            super().__init__(initial_node)

        def set_priority(self, node: PriorityQueueNode):
            """
            Only for clarity - priority already init inside derived node class
            """
            return node.my_heuristic(node.state.TARGET_A)


    def __init__(self, initial_state):
        super().__init__(initial_state, "GBFS")
        self.frontier = self.GBFSFrontier(self.root_node)

    def search(self):
        while self.frontier.open_list:
            current_node = self.frontier.remove_from_frontier()
            if self.is_target(current_node.state):
                return current_node

            for child_state in current_node.state.generate_children():
                if not self.explored.find(child_state):
                    child_node = Node(child_state, current_node)
                    self.frontier.insert_to_frontier(child_node)

            self.explored.insert(current_node.state)
        return None  # No solution found


class AStar(SearchAlgorithm):
    """
    Represent the A* search
    """
    class AStarFrontier(Frontier):
        """
        Derived data structer for overidden priority function
        """

        def __init__(self, initial_node):
            super().__init__(initial_node)

        def set_priority(self, node: PriorityQueueNode):
            # A* specific priority calculation
            return node.cost + \
                min(node.manhattan_distance(node.state.TARGET_A),
                    node.manhattan_distance(node.state.TARGET_B))

    def __init__(self, initial_state):
        super().__init__(initial_state, "A*")
        self.frontier = self.AStarFrontier(self.root_node)

    def search(self):
        while self.frontier.open_list:
            current_node = self.frontier.remove_from_frontier()

            if self.is_target(current_node.state):
                return current_node

            for child_state in current_node.state.generate_children():
                if not self.explored.find(child_state):
                    child_node = Node(child_state, current_node)
                    self.frontier.insert_to_frontier(child_node)

            self.explored.insert(current_node.state)

        return None  # No solution found

def runSearchAlgorithms(algorithm, tiles: List[str]):
    """
    Run the search algorithms and return the results
    """
    tiles = [0 if tile == ' ' else tile for tile in tiles]
    # make sure all are integers
    tiles = [int(tile) for tile in tiles]
    initial_state = State(tiles)
    print(initial_state)
    soulution = algorithm(initial_state).search()
    return soulution.get_path()


def solvePuzzle(tiles: List[str]):
    """
    Run the search algorithms and return the results
    """
    print(tiles)
    initial_state = State(tiles)
    if initial_state.numbers == initial_state.TARGET_A or initial_state.numbers == initial_state.TARGET_B:
        return [len(tiles)-1] if initial_state.numbers == initial_state.TARGET_A else [0]
    print(initial_state)
    path = AStar(initial_state).search().get_path()
    print(str(path))
    # return without the brackets
    return str(path)


def main():
    """
    parse input and run algorithms
    """
    if len(sys.argv) < 9 or 12 < len(sys.argv):
        print(
            f"Usage: python Tiles.py <9 space-separated numbers representing the state>: {len(sys.argv)}")
        sys.exit(1)

    try:
        initial_numbers = [int(num) for num in sys.argv[1:]]
        initial_state = State(initial_numbers)
    except ValueError:
        print("All arguments must be integers.")
        sys.exit(1)

    print(BFS(initial_state))
    print(IDDFS(initial_state))
    print(GBFS(initial_state))
    print(AStar(initial_state))


if __name__ == "__main__":
    main()
