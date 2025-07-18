"""
8-Puzzle Problem:
Place the blank tile in the first position and arrange the remaining 8 tiles in order.
Formulate the problem, or use the formulation discussed in class, to display the sequence of 
steps required to solve the puzzle from a given initial board configuration, as well as the total number of steps.
Use breadth-first search with pruning of already evaluated states.

Puzzles to be tested:

puzzle 1 = (4, 6, 2, 8, 1, 3, 7, 5, 0)
puzzle 2 = (6, 4, 2, 8, 1, 3, 7, 5, 0)
puzzle 3 = Your choice
puzzle 4 = Your choice
"""
from collections import deque

class Node:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth

def is_solvable(state):
    puzzle_pieces = [tile for tile in state if tile != 0]
    inversions = 0
    for i in range(len(puzzle_pieces)):
        for j in range(i + 1, len(puzzle_pieces)):
            if puzzle_pieces[i] > puzzle_pieces[j]:
                inversions += 1
    return inversions % 2 == 0

def get_successors(state):
    successors = []
    blank_index = state.index(0)
    row, col = divmod(blank_index, 3)

    moves = [('Up', -1, 0), ('Down', 1, 0), ('Left', 0, -1), ('Right', 0, 1)]

    for move_name, d_row, d_col in moves:
        new_row, new_col = row + d_row, col + d_col

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state_list = list(state)
            new_blank_index = new_row * 3 + new_col
            
            new_state_list[blank_index], new_state_list[new_blank_index] = \
                new_state_list[new_blank_index], new_state_list[blank_index]
            
            successors.append((move_name, tuple(new_state_list)))
            
    return successors

def reconstruct_path(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()
    return path

def solve_puzzle(initial_board):
    initial_state = initial_board
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    if not is_solvable(initial_state):
        return None, -1, "Puzzle is not solvable."

    if initial_state == goal_state:
        return [Node(initial_state)], 0, "The puzzle is already in the goal state."

    queue = deque([Node(initial_state)])
    visited = {initial_state}

    while queue:
        current_node = queue.popleft()

        for move, new_state in get_successors(current_node.state):
            if new_state not in visited:
                new_node = Node(state=new_state, parent=current_node, move=move, depth=current_node.depth + 1)

                if new_state == goal_state:
                    solution_path = reconstruct_path(new_node)
                    return solution_path, len(solution_path) - 1, "Solution found!"
                
                visited.add(new_state)
                queue.append(new_node)

    return None, -1, "Could not find a solution."

def print_board_state(state):
    for i in range(0, 9, 3):
        row_str = ' '.join(map(str, state[i:i+3])).replace('0', ' ')
        print(f"   [{row_str}]")


def print_solution(puzzle_name, initial_board):
    print(f"--- Solving: {puzzle_name} ---")
    
    print("Initial Board:")
    initial_state_tuple = initial_board
    print_board_state(initial_state_tuple)
    
    solution_path, steps, message = solve_puzzle(initial_board)
    
    print(f"\n{message}")
    
    if solution_path:
        if steps > 0:
            print(f"  Total steps: {steps}")
            print("\n--- Step Sequence ---")
            for i in range(1, len(solution_path)):
                node = solution_path[i]
                print(f"\nStep {i}: Move {node.move}")
                print_board_state(node.state)
            print("\n--- End of Sequence ---")
            
    print("-" * (len(puzzle_name) + 20) + "\n")


if __name__ == '__main__':
    # --- Puzzles to be tested ---

    # 1. First puzzle (unsolvable)
    puzzle1 = (4, 6, 2, 8, 1, 3, 7, 5, 0)

    # 2. Second puzzle (solvable)
    puzzle2 = (6, 4, 2, 8, 1, 3, 7, 5, 0)

    # 3. Third puzzle (custom choice)
    puzzle3 = (1, 2, 3, 0, 4, 5, 6, 7, 8)

    # 4. Fourth puzzle (custom choice - already solved)
    puzzle4 = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    print_solution("Puzzle 1", puzzle1)
    print_solution("Puzzle 2", puzzle2)
    print_solution("Puzzle 3", puzzle3)
    print_solution("Puzzle 4", puzzle4)