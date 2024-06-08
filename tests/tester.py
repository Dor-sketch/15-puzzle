import random
from Tiles import State, BFS, IDDFS, GBFS, AStar, TARGET_A, TARGET_B, PriorityQueueNode, Node

class PuzzleTester:
    def __init__(self, algorithms):
        self.algorithms = algorithms
        self.solutions = {}

    @staticmethod
    def generate_random_state(size=9):
        state = list(range(size))
        random.shuffle(state)
        return state

    @staticmethod
    def generate_solvable_state(num_moves=20):
        # seed the random number generator
        random.seed()
        current_state = State(TARGET_A)
        for _ in range(num_moves):
            children = current_state.generate_children()
            current_state = random.choice(children)
        return current_state.numbers


    def test_random_states(self, num_tests=40):
        for i in range(num_tests):
            random_state = PuzzleTester.generate_solvable_state()
            optimal_length = (BFS(State(random_state)).search().cost)
            if optimal_length != 0:
                for algo in self.algorithms:
                    algo_instance = algo(State(random_state))
                    # print(
                        # f"Algorithm: {algo.__name__}, Cost: {algo_instance.search().cost} Solution: {'Found' if solution else 'Not found'}")

                    if (algo(State(random_state)).search().cost) != optimal_length:
                        print(f"\n{i}. Testing state:\n{State(random_state)}\noptimal length is {optimal_length}")
                        print(algo(State(random_state)).search().back_track_h())
                        print(algo_instance)
                        print()
                        print(
                            f"Problem - found path of {algo_instance.search().cost}")
                    else:
                        print(f"Test {i} Pass")



# Example Usage
if __name__ == "__main__":
    # print(PriorityQueueNode(Node(State([0, 1, 4, 6, 3, 2, 7, 8, 5]))).my_heuristic())
    tester = PuzzleTester([BFS, GBFS, AStar])
    tester.test_random_states(500)  # Testing 5 random states
